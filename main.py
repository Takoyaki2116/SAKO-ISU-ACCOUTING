from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from datebase import BusinessPartner
from datebase import Claim
from datebase import Receipt
from datebase import Quotation
from datebase import Inquiry
from peewee import *
from werkzeug.utils import secure_filename
import os

import numpy as np
from PIL import Image

import torch
import cv2
import io

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 基準物体の寸法（例: ペットボトルの幅 6.5cm）
REFERENCE_WIDTH_CM = 6.5

def calculate_real_size(detected_object, reference_object):
    """実寸を計算するためのスケーリング処理（幅と高さ）"""
    # 検出された基準物体のピクセル幅とピクセル高さを取得
    reference_pixel_width = reference_object['xmax'] - reference_object['xmin']
    reference_pixel_height = reference_object['ymax'] - reference_object['ymin']
    
    # ピクセル幅からスケールを計算
    scale_factor_width = REFERENCE_WIDTH_CM / reference_pixel_width
    
    # 対象物のピクセル寸法（幅と高さ）を取得
    object_pixel_width = detected_object['xmax'] - detected_object['xmin']
    object_pixel_height = detected_object['ymax'] - detected_object['ymin']
    
    # 幅と高さの実寸を計算
    real_width = object_pixel_width * scale_factor_width  # 実際の幅（cm）
    real_height = object_pixel_height * scale_factor_width  # 実際の高さ（cm）
    
    return real_width, real_height


@app.route('/')
def index():
  return redirect('/top')


@app.route("/top")
def top():
  return render_template("top.html")


@app.route("/login")
def login():
  return render_template("login.html")


@app.route("/claim")
def claim():
  claim = Claim.select()
  return render_template("claim.html", claim=claim)


@app.route("/claim_create")
def claim_create():
  business_partner = BusinessPartner.select()
  return render_template("claim_create.html",
                         business_partner=business_partner)


@app.route("/claim_edit/<id>")
def claim_edit(id):
  claim = Claim.get(id=id)
  return render_template("claim_edit.html", claim=claim)


@app.route("/receipt")
def receipt():
  receipt = Receipt.select()
  return render_template("receipt.html", receipt=receipt)


@app.route("/receipt_create")
def receipt_create():
  business_partner = BusinessPartner.select()
  return render_template("receipt_create.html",
                         business_partner=business_partner)


@app.route("/receipt_edit/<id>")
def receipt_edit(id):
  receipt = Receipt.get(id=id)
  return render_template("receipt_edit.html", receipt=receipt)


@app.route("/quotation")
def quotation():
  quotation = Quotation.select()
  return render_template("quotation.html", quotation=quotation)


@app.route("/quotation_create")
def quotation_create():
  business_partner = BusinessPartner.select()
  return render_template("quotation_create.html",
                         business_partner=business_partner)


@app.route("/quotation_edit/<id>")
def quotation_edit(id):
  quotation = Quotation.get(id=id)
  return render_template("quotation_edit.html", quotation=quotation)


@app.route("/business_partner")
def business_partner():
  business_partners = BusinessPartner.select()
  return render_template("business_partner.html",
                         business_partners=business_partners)


@app.route("/business_partner_create")
def business_partner_create():
  return render_template("business_partner_create.html")


@app.route("/business_partner_edit/<id>")
def business_partner_edit(id):
  business_partner = BusinessPartner.get(id=id)
  return render_template("business_partner_edit.html",
                         business_partner=business_partner)


@app.route("/new_business_partner", methods=["POST"])
def new_business_partner():
  name = request.form.get("name")
  address = request.form.get("address")
  contact = request.form.get("contact")
  remarks = request.form.get("remarks")

  bp = BusinessPartner(name=name,
                       address=address,
                       contact=contact,
                       remarks=remarks)
  bp.save()
  return redirect("/business_partner")


@app.route("/new_claim", methods=["POST"])
def new_claim():
  business_partner = request.form.get("business_partner")
  subject = request.form.get("subject")
  day = request.form.get("day")
  payment = request.form.get("payment")
  amount = request.form.get("amount")
  status = request.form.get("status")

  C = Claim(subject=subject,
            day=day,
            payment=payment,
            amount=amount,
            status=status,
            business_partner=business_partner)
  C.save()
  return redirect("/claim")


@app.route("/new_receipt", methods=["POST"])
def new_raceipt():
  business_partner = request.form.get("business_partner")
  subject = request.form.get("subject")
  day = request.form.get("day")
  amount = request.form.get("amount")
  status = request.form.get("status")

  R = Receipt(subject=subject,
              day=day,
              amount=amount,
              status=status,
              business_partner=business_partner)
  R.save()
  return redirect("/receipt")

def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
@app.route("/new_quotation", methods=["POST"])
def new_quotation():
  business_partner = request.form.get("business_partner")
  subject = request.form.get("subject")
  day = request.form.get("day")
  amount = request.form.get("amount")
  status = request.form.get("status")

  Q = Quotation(subject=subject,
                day=day,
                amount=amount,
                status=status,
                business_partner=business_partner)
  Q.save()
  return redirect("/quotation")


@app.route("/measure")
def measure():
  return render_template("measure.html")

@app.route("/measure_upload", methods=["POST"])
def measure_upload():
  if request.method== 'POST':
    name = request.form.get("name")
    furigana = request.form.get("furigana")
    mail = request.form.get("mail")
    detail = request.form.get("detail")

    I= Inquiry(name=name,
                  furigana=furigana,
                  mail=mail,
                  detail=detail,)
    I.save()
    if 'file' not in request.files:
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      return redirect(request.url)
    if file and allowed_file(file.filename):
      # filename = secure_filename(file.filename)
      # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      img_bytes = file.read()
      img = Image.open(io.BytesIO(img_bytes))
      img_array = np.array(img)
      model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
      results = model(img_array)
      detections = results
      reference_object = None
      for i, row in detections.pandas().xyxy[0].iterrows():
          if row['name'] == 'bottle':  # ペットボトルを基準物体として検出
              reference_object = row
              break
      if reference_object is None:
            return "基準物体が見つかりませんでした"
      # 検出された物体ごとの寸法を計算
      objects_info = []
      for i, row in detections.pandas().xyxy[0].iterrows():
          if row['name'] != 'bottle':  # 基準物体以外を処理
              real_width, real_height = calculate_real_size(row, reference_object)
              objects_info.append({
                  'name': row['name'],
                  'width': real_width,
                  'height': real_height
              })
      
      # 結果画像を保存
      if isinstance(UPLOAD_FOLDER, str) and isinstance(file.filename, str):
          results_image_path = os.path.join(UPLOAD_FOLDER, file.filename)
          img_with_boxes = detections.render()[0]  # 検出結果を画像に描画
          cv2.imwrite(results_image_path, img_with_boxes)  # OpenCVを使用して画像を保存
      else:
          print("Error: UPLOAD_FOLDER or file.filename is not a string")
      return redirect("/measure")
    return redirect("/measure")

app.run(host='0.0.0.0', port=5001)

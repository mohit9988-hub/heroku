import MultipartPostHandler
import urllib2
from api import *
import time
import json
import copy
from flask import Flask, request, redirect, url_for, Response
from templates import *
import copy
import documentx
import os
import sys
import fdfgen


app = Flask(__name__)

auth = 'e488f89bc2b3d62957860f74f1a367d0'

CLIENT_ID = '94f790d3236110dd24b7'

ID = '2282460000001349782'
authtoken = '193282832981094154354b8a9a0940a5'


def formswitch(rform):
    if "medicaiddelivery" in rform:
        documentx.MedicaidDelivery(rform)
    if "utahpowerchecklist" in rform:
        documentx.PowerChairTrainingChecklist(rform)
    if "productdescription" in rform:
        documentx.DetailedProductDescription(rform)
    if "deliveryticket" in rform:
        documentx.DeliveryTicket(rform)
    if "wheelchaireval" in rform:
        documentx.WheelchairEval(rform)
    if "priorauth" in rform:
        documentx.PriorAuth(rform)
    if "customequipmentmeasurementsheet" in rform:
        documentx.EquipmentMeasurementSheet(rform)
    if "idaho_mcd_pa" in rform:
        documentx.idaho_mcd_pa(rform)
    if "nv_wheel_repair" in rform:
        documentx.nv_wheel_repair(rform)
    if "id_dmerequest" in rform:
        documentx.ID_DMERequest(rform)
    if "mobility_evaluation_template_idaho" in rform:
        documentx.mobility_evaluation_template_idaho(rform)
    if "nv_dme_prior_auth" in rform:
        documentx.nv_dme_prior_auth(rform)
    if "nv_mobility_assessment_pa" in rform:
        documentx.nv_mobility_assessment_pa(rform)


@app.route("/", methods=['POST'])
def webhook():
    rform = request.form
    print rform
    if rform['auth'] != auth:
        return "error"
    formswitch(rform)
    return "hello creator"


if __name__ == '__main__':
    app.run()

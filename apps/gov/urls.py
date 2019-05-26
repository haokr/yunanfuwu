from flask import Blueprint, request
import apps.gov.view as view

gov = Blueprint('equipment', __name__)
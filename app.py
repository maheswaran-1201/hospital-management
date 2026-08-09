from flask import Flask, jsonify, request, render_template
from backend.doctor import (
    get_all_doctors, get_doctor_by_id, add_doctor_api, update_doctor_api, delete_doctor_api
)
from backend.patient import (
    get_all_patients, get_patient_by_id, add_patient_api, update_patient_api, delete_patient_api
)
from backend.staff import (
    get_all_staff, get_staff_by_id, add_staff_api, update_staff_api, delete_staff_api
)
from backend.medicine import (
    get_all_medicines, get_medicine_by_id, add_medicine_api, update_medicine_api, delete_medicine_api
)
from backend.machinery import (
    get_all_machinery, get_machinery_by_id, add_machinery_api, update_machinery_api, delete_machinery_api
)
from datetime import datetime

app = Flask(__name__)

# Utility function for numeric validation
def is_numeric(val):
    if val is None or str(val).strip() == "":
        return False
    # Strip commas e.g. "10,12,000"
    cleaned = str(val).replace(",", "").replace("₹", "").replace("$", "").strip()
    try:
        float(cleaned)
        return True
    except ValueError:
        return False

# Render Dashboard HTML page
@app.route("/")
def index():
    return render_template("index.html")

# Dashboard Stats API
@app.route("/api/dashboard", methods=["GET"])
def get_dashboard_stats():
    try:
        doctors = get_all_doctors()
        patients = get_all_patients()
        staff = get_all_staff()
        medicines = get_all_medicines()
        machinery = get_all_machinery()

        # Calculate expiring medicines count (within 90 days or already expired)
        expiring_meds_count = 0
        now = datetime.now()
        for med in medicines:
            exp_str = med.get("expiryDate", "")
            if exp_str:
                for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
                    try:
                        exp_dt = datetime.strptime(exp_str, fmt)
                        days_diff = (exp_dt - now).days
                        if days_diff <= 90:
                            expiring_meds_count += 1
                        break
                    except ValueError:
                        continue

        # Calculate low stock machinery count (quantity <= 5)
        low_stock_machinery_count = 0
        for m in machinery:
            qty_str = str(m.get("quantity", "0")).strip()
            try:
                qty = int(qty_str)
                if qty <= 5:
                    low_stock_machinery_count += 1
            except ValueError:
                pass

        recent_patients = patients[-5:] if len(patients) >= 5 else patients
        recent_patients = list(reversed(recent_patients))

        return jsonify({
            "success": True,
            "data": {
                "doctorsCount": len(doctors),
                "patientsCount": len(patients),
                "staffCount": len(staff),
                "medicinesCount": len(medicines),
                "machineryCount": len(machinery),
                "expiringMedicinesCount": expiring_meds_count,
                "lowStockMachineryCount": low_stock_machinery_count,
                "recentPatients": recent_patients
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# =========================================================================
# DOCTORS REST API
# =========================================================================

@app.route("/api/doctors", methods=["GET"])
def api_get_doctors():
    try:
        doctors = get_all_doctors()
        return jsonify({"success": True, "data": doctors}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/doctors/<doc_id>", methods=["GET"])
def api_get_doctor(doc_id):
    try:
        doctor = get_doctor_by_id(doc_id)
        if not doctor:
            return jsonify({"success": False, "message": "Doctor not found."}), 404
        return jsonify({"success": True, "data": doctor}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/doctors", methods=["POST"])
def api_add_doctor():
    try:
        data = request.get_json() or {}
        doc_id = str(data.get("id", "")).strip()
        name = str(data.get("name", "")).strip()
        age = str(data.get("age", "")).strip()
        salary = str(data.get("salary", "")).strip()

        if not doc_id:
            return jsonify({"success": False, "message": "Doctor ID is required."}), 400
        if not name:
            return jsonify({"success": False, "message": "Doctor Name is required."}), 400
        if age and not is_numeric(age):
            return jsonify({"success": False, "message": "Age must be numeric."}), 400
        if salary and not is_numeric(salary):
            return jsonify({"success": False, "message": "Salary must be numeric."}), 400

        success, result = add_doctor_api(data)
        if not success:
            return jsonify({"success": False, "message": result}), 409 if "already exists" in result else 400
        return jsonify({"success": True, "message": "Doctor added successfully.", "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/doctors/<doc_id>", methods=["PUT"])
def api_update_doctor(doc_id):
    try:
        data = request.get_json() or {}
        age = str(data.get("age", "")).strip()
        salary = str(data.get("salary", "")).strip()

        if age and not is_numeric(age):
            return jsonify({"success": False, "message": "Age must be numeric."}), 400
        if salary and not is_numeric(salary):
            return jsonify({"success": False, "message": "Salary must be numeric."}), 400

        success, result = update_doctor_api(doc_id, data)
        if not success:
            status = 404 if "not found" in result else (409 if "already exists" in result else 400)
            return jsonify({"success": False, "message": result}), status
        return jsonify({"success": True, "message": "Doctor updated successfully.", "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/doctors/<doc_id>", methods=["DELETE"])
def api_delete_doctor(doc_id):
    try:
        success, result = delete_doctor_api(doc_id)
        if not success:
            return jsonify({"success": False, "message": result}), 404
        return jsonify({"success": True, "message": "Doctor deleted successfully.", "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# =========================================================================
# PATIENTS REST API
# =========================================================================

@app.route("/api/patients", methods=["GET"])
def api_get_patients():
    try:
        patients = get_all_patients()
        return jsonify({"success": True, "data": patients}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/patients/<pat_id>", methods=["GET"])
def api_get_patient(pat_id):
    try:
        patient = get_patient_by_id(pat_id)
        if not patient:
            return jsonify({"success": False, "message": "Patient not found."}), 404
        return jsonify({"success": True, "data": patient}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/patients", methods=["POST"])
def api_add_patient():
    try:
        data = request.get_json() or {}
        pat_id = str(data.get("id", "")).strip()
        name = str(data.get("name", "")).strip()
        age = str(data.get("age", "")).strip()

        if not pat_id:
            return jsonify({"success": False, "message": "Patient ID is required."}), 400
        if not name:
            return jsonify({"success": False, "message": "Patient Name is required."}), 400
        if age and not is_numeric(age):
            return jsonify({"success": False, "message": "Age must be numeric."}), 400

        success, result = add_patient_api(data)
        if not success:
            return jsonify({"success": False, "message": result}), 409 if "already exists" in result else 400
        return jsonify({"success": True, "message": "Patient added successfully.", "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/patients/<pat_id>", methods=["PUT"])
def api_update_patient(pat_id):
    try:
        data = request.get_json() or {}
        age = str(data.get("age", "")).strip()
        if age and not is_numeric(age):
            return jsonify({"success": False, "message": "Age must be numeric."}), 400

        success, result = update_patient_api(pat_id, data)
        if not success:
            status = 404 if "not found" in result else (409 if "already exists" in result else 400)
            return jsonify({"success": False, "message": result}), status
        return jsonify({"success": True, "message": "Patient updated successfully.", "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/patients/<pat_id>", methods=["DELETE"])
def api_delete_patient(pat_id):
    try:
        success, result = delete_patient_api(pat_id)
        if not success:
            return jsonify({"success": False, "message": result}), 404
        return jsonify({"success": True, "message": "Patient deleted successfully.", "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# =========================================================================
# STAFF REST API
# =========================================================================

@app.route("/api/staff", methods=["GET"])
def api_get_staff():
    try:
        staff_members = get_all_staff()
        return jsonify({"success": True, "data": staff_members}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/staff/<staff_id>", methods=["GET"])
def api_get_staff_by_id(staff_id):
    try:
        member = get_staff_by_id(staff_id)
        if not member:
            return jsonify({"success": False, "message": "Staff member not found."}), 404
        return jsonify({"success": True, "data": member}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/staff", methods=["POST"])
def api_add_staff():
    try:
        data = request.get_json() or {}
        staff_id = str(data.get("id", "")).strip()
        name = str(data.get("name", "")).strip()
        age = str(data.get("age", "")).strip()
        salary = str(data.get("salary", "")).strip()

        if not staff_id:
            return jsonify({"success": False, "message": "Staff ID is required."}), 400
        if not name:
            return jsonify({"success": False, "message": "Staff Name is required."}), 400
        if age and not is_numeric(age):
            return jsonify({"success": False, "message": "Age must be numeric."}), 400
        if salary and not is_numeric(salary):
            return jsonify({"success": False, "message": "Salary must be numeric."}), 400

        success, result = add_staff_api(data)
        if not success:
            return jsonify({"success": False, "message": result}), 409 if "already exists" in result else 400
        return jsonify({"success": True, "message": "Staff added successfully.", "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/staff/<staff_id>", methods=["PUT"])
def api_update_staff(staff_id):
    try:
        data = request.get_json() or {}
        age = str(data.get("age", "")).strip()
        salary = str(data.get("salary", "")).strip()

        if age and not is_numeric(age):
            return jsonify({"success": False, "message": "Age must be numeric."}), 400
        if salary and not is_numeric(salary):
            return jsonify({"success": False, "message": "Salary must be numeric."}), 400

        success, result = update_staff_api(staff_id, data)
        if not success:
            status = 404 if "not found" in result else (409 if "already exists" in result else 400)
            return jsonify({"success": False, "message": result}), status
        return jsonify({"success": True, "message": "Staff updated successfully.", "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/staff/<staff_id>", methods=["DELETE"])
def api_delete_staff(staff_id):
    try:
        success, result = delete_staff_api(staff_id)
        if not success:
            return jsonify({"success": False, "message": result}), 404
        return jsonify({"success": True, "message": "Staff deleted successfully.", "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# =========================================================================
# MEDICINES REST API
# =========================================================================

@app.route("/api/medicines", methods=["GET"])
def api_get_medicines():
    try:
        medicines = get_all_medicines()
        return jsonify({"success": True, "data": medicines}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/medicines/<med_id>", methods=["GET"])
def api_get_medicine(med_id):
    try:
        medicine = get_medicine_by_id(med_id)
        if not medicine:
            return jsonify({"success": False, "message": "Medicine not found."}), 404
        return jsonify({"success": True, "data": medicine}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/medicines", methods=["POST"])
def api_add_medicine():
    try:
        data = request.get_json() or {}
        med_id = str(data.get("id", "")).strip()
        name = str(data.get("name", "")).strip()
        price = str(data.get("price", "")).strip()

        if not med_id:
            return jsonify({"success": False, "message": "Medicine ID is required."}), 400
        if not name:
            return jsonify({"success": False, "message": "Medicine Name is required."}), 400
        if price and not is_numeric(price):
            return jsonify({"success": False, "message": "Price must be numeric."}), 400

        success, result = add_medicine_api(data)
        if not success:
            return jsonify({"success": False, "message": result}), 409 if "already exists" in result else 400
        return jsonify({"success": True, "message": "Medicine added successfully.", "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/medicines/<med_id>", methods=["PUT"])
def api_update_medicine(med_id):
    try:
        data = request.get_json() or {}
        price = str(data.get("price", "")).strip()
        if price and not is_numeric(price):
            return jsonify({"success": False, "message": "Price must be numeric."}), 400

        success, result = update_medicine_api(med_id, data)
        if not success:
            status = 404 if "not found" in result else (409 if "already exists" in result else 400)
            return jsonify({"success": False, "message": result}), status
        return jsonify({"success": True, "message": "Medicine updated successfully.", "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/medicines/<med_id>", methods=["DELETE"])
def api_delete_medicine(med_id):
    try:
        success, result = delete_medicine_api(med_id)
        if not success:
            return jsonify({"success": False, "message": result}), 404
        return jsonify({"success": True, "message": "Medicine deleted successfully.", "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# =========================================================================
# MACHINERY REST API
# =========================================================================

@app.route("/api/machinery", methods=["GET"])
def api_get_machinery():
    try:
        machinery = get_all_machinery()
        return jsonify({"success": True, "data": machinery}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/machinery/<mac_id>", methods=["GET"])
def api_get_machinery_by_id(mac_id):
    try:
        machine = get_machinery_by_id(mac_id)
        if not machine:
            return jsonify({"success": False, "message": "Machinery not found."}), 404
        return jsonify({"success": True, "data": machine}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/machinery", methods=["POST"])
def api_add_machinery():
    try:
        data = request.get_json() or {}
        mac_id = str(data.get("id", "")).strip()
        name = str(data.get("name", "")).strip()
        quantity = str(data.get("quantity", "")).strip()
        price = str(data.get("price", "")).strip()

        if not mac_id:
            return jsonify({"success": False, "message": "Machinery ID is required."}), 400
        if not name:
            return jsonify({"success": False, "message": "Machinery Name is required."}), 400
        if quantity and not is_numeric(quantity):
            return jsonify({"success": False, "message": "Quantity must be numeric."}), 400
        if price and not is_numeric(price):
            return jsonify({"success": False, "message": "Price must be numeric."}), 400

        success, result = add_machinery_api(data)
        if not success:
            return jsonify({"success": False, "message": result}), 409 if "already exists" in result else 400
        return jsonify({"success": True, "message": "Machinery added successfully.", "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/machinery/<mac_id>", methods=["PUT"])
def api_update_machinery(mac_id):
    try:
        data = request.get_json() or {}
        quantity = str(data.get("quantity", "")).strip()
        price = str(data.get("price", "")).strip()

        if quantity and not is_numeric(quantity):
            return jsonify({"success": False, "message": "Quantity must be numeric."}), 400
        if price and not is_numeric(price):
            return jsonify({"success": False, "message": "Price must be numeric."}), 400

        success, result = update_machinery_api(mac_id, data)
        if not success:
            status = 404 if "not found" in result else (409 if "already exists" in result else 400)
            return jsonify({"success": False, "message": result}), status
        return jsonify({"success": True, "message": "Machinery updated successfully.", "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/machinery/<mac_id>", methods=["DELETE"])
def api_delete_machinery(mac_id):
    try:
        success, result = delete_machinery_api(mac_id)
        if not success:
            return jsonify({"success": False, "message": result}), 404
        return jsonify({"success": True, "message": "Machinery deleted successfully.", "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

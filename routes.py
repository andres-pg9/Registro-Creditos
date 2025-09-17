from flask import Blueprint, request, jsonify
from extensions import db
from models import Credito

creditos_bp = Blueprint('creditos', __name__)

# Crear un crédito
@creditos_bp.route('/creditos', methods=['POST'])
def crear_credito():
    data = request.json
    nuevo_credito = Credito(
        cliente=data['cliente'],
        monto=data['monto'],
        tasa_interes=data['tasa_interes'],
        plazo=data['plazo'],
        fecha_otorgamiento=data['fecha_otorgamiento']
    )
    db.session.add(nuevo_credito)
    db.session.commit()
    return jsonify({"message": "Crédito creado exitosamente"}), 201

# Leer todos los créditos
@creditos_bp.route('/creditos', methods=['GET'])
def listar_creditos():
    creditos = Credito.query.all()
    resultado = []
    for c in creditos:
        resultado.append({
            "id": c.id,
            "cliente": c.cliente,
            "monto": c.monto,
            "tasa_interes": c.tasa_interes,
            "plazo": c.plazo,
            "fecha_otorgamiento": c.fecha_otorgamiento
        })
    return jsonify(resultado)

# Actualizar un crédito
@creditos_bp.route('/creditos/<int:id>', methods=['PUT'])
def actualizar_credito(id):
    credito = Credito.query.get_or_404(id)
    data = request.json
    credito.cliente = data.get('cliente', credito.cliente)
    credito.monto = data.get('monto', credito.monto)
    credito.tasa_interes = data.get('tasa_interes', credito.tasa_interes)
    credito.plazo = data.get('plazo', credito.plazo)
    credito.fecha_otorgamiento = data.get('fecha_otorgamiento', credito.fecha_otorgamiento)
    db.session.commit()
    return jsonify({"message": "Crédito actualizado exitosamente"})

# Eliminar un crédito
@creditos_bp.route('/creditos/<int:id>', methods=['DELETE'])
def eliminar_credito(id):
    credito = Credito.query.get_or_404(id)
    db.session.delete(credito)
    db.session.commit()
    return jsonify({"message": "Crédito eliminado exitosamente"})

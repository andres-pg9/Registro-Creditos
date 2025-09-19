from flask import Blueprint, request, jsonify
from extensions import db
from models import Credito

creditos_bp = Blueprint('creditos', __name__)


@creditos_bp.route('/creditos', methods=['POST'])
def crear_credito():
    """Crea un nuevo crédito"""
    try:
        data = request.json
        
        # Validaciones básicas
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400
            
        campos_requeridos = ['cliente', 'monto', 'tasa_interes', 'plazo', 'fecha_otorgamiento']
        for campo in campos_requeridos:
            if not data.get(campo):
                return jsonify({"error": f"El campo '{campo}' es requerido"}), 400
        
        # Validar rangos
        monto = float(data['monto'])
        tasa = float(data['tasa_interes'])
        plazo = int(data['plazo'])
        
        if monto <= 0 or monto > 10000000:
            return jsonify({"error": "Monto debe estar entre $1 y $10,000,000"}), 400
        if tasa < 0 or tasa > 100:
            return jsonify({"error": "Tasa debe estar entre 0% y 100%"}), 400
        if plazo < 1 or plazo > 360:
            return jsonify({"error": "Plazo debe estar entre 1 y 360 meses"}), 400
        
        # Crear crédito
        nuevo_credito = Credito(
            cliente=data['cliente'].strip(),
            monto=monto,
            tasa_interes=tasa,
            plazo=plazo,
            fecha_otorgamiento=data['fecha_otorgamiento']
        )
        
        db.session.add(nuevo_credito)
        db.session.commit()
        
        return jsonify({"message": "Crédito creado exitosamente"}), 201
        
    except ValueError:
        return jsonify({"error": "Datos numéricos inválidos"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor"}), 500

@creditos_bp.route('/creditos', methods=['GET'])
def listar_creditos():
    """Lista todos los créditos"""
    try:
        creditos = Credito.query.all()
        resultado = []
        for c in creditos:
            resultado.append({
                "id": c.id,
                "cliente": c.cliente,
                "monto": float(c.monto),
                "tasa_interes": float(c.tasa_interes),
                "plazo": c.plazo,
                "fecha_otorgamiento": str(c.fecha_otorgamiento)
            })
        return jsonify(resultado)
    except Exception:
        return jsonify({"error": "Error al consultar créditos"}), 500

@creditos_bp.route('/creditos/<int:id>', methods=['PUT'])
def actualizar_credito(id):
    """Actualiza un crédito existente"""
    try:
        credito = Credito.query.get_or_404(id)
        data = request.json
        
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400
        
        # Validar si se envían datos numéricos
        if 'monto' in data:
            monto = float(data['monto'])
            if monto <= 0 or monto > 10000000:
                return jsonify({"error": "Monto inválido"}), 400
            credito.monto = monto
            
        if 'tasa_interes' in data:
            tasa = float(data['tasa_interes'])
            if tasa < 0 or tasa > 100:
                return jsonify({"error": "Tasa inválida"}), 400
            credito.tasa_interes = tasa
            
        if 'plazo' in data:
            plazo = int(data['plazo'])
            if plazo < 1 or plazo > 360:
                return jsonify({"error": "Plazo inválido"}), 400
            credito.plazo = plazo
        
        # Actualizar otros campos
        if 'cliente' in data:
            credito.cliente = data['cliente'].strip()
        if 'fecha_otorgamiento' in data:
            credito.fecha_otorgamiento = data['fecha_otorgamiento']
        
        db.session.commit()
        return jsonify({"message": "Crédito actualizado exitosamente"})
        
    except ValueError:
        return jsonify({"error": "Datos numéricos inválidos"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor"}), 500

@creditos_bp.route('/creditos/<int:id>', methods=['DELETE'])
def eliminar_credito(id):
    """Elimina un crédito"""
    try:
        credito = Credito.query.get_or_404(id)
        db.session.delete(credito)
        db.session.commit()
        return jsonify({"message": "Crédito eliminado exitosamente"})
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor"}), 500

# ========================================
# ENDPOINTS DE ANÁLISIS
# ========================================

@creditos_bp.route('/creditos/total', methods=['GET'])
def total_creditos():
    """Obtiene el total de créditos otorgados"""
    try:
        total = db.session.query(db.func.sum(Credito.monto)).scalar() or 0
        return jsonify({"total_creditos": float(total)})
    except Exception:
        return jsonify({"error": "Error al consultar total"}), 500

@creditos_bp.route('/creditos/por_cliente', methods=['GET'])
def creditos_por_cliente():
    """Obtiene créditos agrupados por cliente"""
    try:
        resultados = db.session.query(
            Credito.cliente,
            db.func.sum(Credito.monto).label('total')
        ).group_by(Credito.cliente).all()

        data = [{"cliente": r[0], "total": float(r[1])} for r in resultados]
        return jsonify(data)
    except Exception:
        return jsonify({"error": "Error al consultar datos por cliente"}), 500

@creditos_bp.route('/creditos/por_rangos', methods=['GET'])
def creditos_por_rangos():
    """Obtiene distribución por rangos de montos"""
    try:
        rango1 = db.session.query(db.func.count(Credito.id)).filter(Credito.monto <= 5000).scalar() or 0
        rango2 = db.session.query(db.func.count(Credito.id)).filter(
            Credito.monto.between(5001, 15000)
        ).scalar() or 0
        rango3 = db.session.query(db.func.count(Credito.id)).filter(Credito.monto > 15000).scalar() or 0

        return jsonify({
            "0 - 5000": rango1,
            "5001 - 15000": rango2,
            "15001+": rango3
        })
    except Exception:
        return jsonify({"error": "Error al consultar rangos"}), 500

@creditos_bp.route('/creditos/estadisticas', methods=['GET'])
def estadisticas_generales():
    """Obtiene estadísticas generales del sistema"""
    try:
        total_creditos = db.session.query(db.func.count(Credito.id)).scalar() or 0
        monto_total = db.session.query(db.func.sum(Credito.monto)).scalar() or 0
        clientes_unicos = db.session.query(
            db.func.count(db.func.distinct(Credito.cliente))
        ).scalar() or 0
        monto_promedio = db.session.query(db.func.avg(Credito.monto)).scalar() or 0

        return jsonify({
            "total_creditos": total_creditos,
            "monto_total": float(monto_total),
            "clientes_unicos": clientes_unicos,
            "monto_promedio": float(monto_promedio)
        })
    except Exception:
        return jsonify({"error": "Error al consultar estadísticas"}), 500
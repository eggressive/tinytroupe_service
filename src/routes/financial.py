"""
Financial data routes for TinyTroupe Service
"""
from flask import Blueprint, jsonify, request
from src.services.financial_service import FinancialService

financial_bp = Blueprint('financial', __name__)
financial_service = FinancialService()

@financial_bp.route('/<symbol>', methods=['GET'])
def get_financial_data(symbol):
    """Get financial data for a specific symbol"""
    try:
        data = financial_service.get_stock_data(symbol)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@financial_bp.route('/<symbol>/analysis', methods=['GET'])
def get_stock_analysis(symbol):
    """Get advisor analysis for a specific stock symbol"""
    try:
        analysis = financial_service.get_stock_analysis(symbol)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

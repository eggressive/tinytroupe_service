"""
Financial data service
"""
import logging
import os
from typing import Dict, Any
import requests
import json

class FinancialService:
    """Service for retrieving and analyzing financial data"""
    
    def __init__(self):
        """Initialize the financial service"""
        self.logger = logging.getLogger(__name__)
        self.yahoo_finance_api_key = os.getenv('YAHOO_FINANCE_API_KEY')
        self.alpha_vantage_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        # Initialize TinyTroupe service for stock analysis
        from src.services.tinytroupe_service import TinyTroupeService
        self.tinytroupe_service = TinyTroupeService()
        
    def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Get financial data for a stock symbol
        
        Args:
            symbol: Stock symbol to get data for
            
        Returns:
            Dictionary containing financial data
        """
        self.logger.info(f"Getting stock data for: {symbol}")
        
        # In a real implementation, you would call the Yahoo Finance or Alpha Vantage API
        # For now, we'll return placeholder data
        
        try:
            # Placeholder for API call
            # if self.yahoo_finance_api_key:
            #     response = requests.get(
            #         f"https://yfapi.net/v6/finance/quote",
            #         params={"symbols": symbol},
            #         headers={"X-API-KEY": self.yahoo_finance_api_key}
            #     )
            #     return response.json()
            
            # Return placeholder data
            return {
                "symbol": symbol,
                "price": 123.45,
                "change": 1.23,
                "change_percent": 1.01,
                "market_cap": "123.45B",
                "pe_ratio": 15.67,
                "dividend_yield": 2.34,
                "52_week_high": 150.00,
                "52_week_low": 100.00,
                "data_source": "Placeholder data (API keys not configured)"
            }
            
        except Exception as e:
            self.logger.error(f"Error getting stock data for {symbol}: {str(e)}")
            raise
    
    def get_stock_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get advisor analysis for a stock symbol
        
        Args:
            symbol: Stock symbol to analyze
            
        Returns:
            Dictionary containing analysis from each advisor
        """
        self.logger.info(f"Getting stock analysis for: {symbol}")
        
        try:
            # Get stock data first
            stock_data = self.get_stock_data(symbol)
            
            # Get analysis from TinyTroupe service
            analysis = self.tinytroupe_service.analyze_stock(symbol)
            
            # Combine data and analysis
            result = {
                "stock_data": stock_data,
                "advisor_analysis": analysis
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting stock analysis for {symbol}: {str(e)}")
            raise

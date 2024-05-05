##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: queries.py
# Capitulo: Flujo de Datos
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 1.0.0 Noviembre 2022
# Descripción:
#
#   Este archivo define las consultas que permiten obtener información 
#   y realizar el llenado de datos del tablero
#
#-------------------------------------------------------------------------
class Queries:

    @staticmethod
    def get_total_products():
        return """
            {
                response(func: has(description)) {
                    count(uid)
                }
            }
        """
        
    @staticmethod
    def get_products_by_period(start_date, end_date):
        query = '''
            {
  var(func: has(invoice)) @filter(ge(date, "'''+start_date+'''") AND le(date, "'''+end_date+'''")) {
    prod as ~bought
  }
    
    response(func: uid(prod)) {
    count: count(uid)
  }
  }
        '''
        return query

    @staticmethod
    def get_total_providers():
        return """
            {
                response(func: has(pid)) {
                    count(uid)
                }
            }
        """
        
    @staticmethod
    def get_providers_by_period(start_date, end_date):
        query = '''
            {
                var(func: has(invoice)) @filter(ge(date, "'''+start_date+'''") AND le(date, "'''+end_date+'''")) {
                    ~bought {
                            prov as sold
                    }
                }
                
                response(func: uid(prov)) {
                    count: count(uid)
                }
            }
        '''
        return query

    @staticmethod
    def get_total_locations():
        return """
            {
                response(func: has(name)) {
                    count(uid)
                }
            }
        """

    @staticmethod
    def get_total_orders():
        return """
            {
                response(func: has(invoice)) {
                    count(uid)
                }
            }
        """
    
    # Added
    @staticmethod
    def get_orders_by_period(start_date, end_date):
        query = '''
            {
                response(func: has(invoice))  @filter(ge(date, "'''+start_date+'''") AND le(date, "'''+end_date+'''")) {
                    count(uid)
                }
            }
        '''
        return query

    @staticmethod
    def get_total_sales():
        return """
            {
                var(func: has(invoice)) {
                    t as total
                }

                response() {
                    total: sum(val(t))
                }
            }
        """
        
    @staticmethod
    def get_sales_by_period(start_date, end_date):
        query = '''
            {
                var(func: has(invoice)) @filter(ge(date, "'''+start_date+'''") AND le(date, "'''+end_date+'''")) {
                    t as total
                }

                response() {
                    total: sum(val(t))
                }
            }
        '''
        return query
    
    @staticmethod
    def get_providers_per_location():
        return """
            {
                response(func: has(name)) {
                    name
                    providers: ~belongs {
                        count(uid)
                    }
                }
            }
        """

    @staticmethod
    def get_sales_per_location():
        return """
            {
                response(func: has(name)){
                    name
                    providers: ~belongs {
                        sold: ~sold {
                            price
                            quantity: count(bought)
                        }
                    }
                }
            }
        """
    
    @staticmethod
    def get_sales_per_location_by_period(start_date, end_date):
        query = '''
            {
                var(func: has(invoice)) @filter(ge(date, "'''+start_date+'''") AND le(date, "'''+end_date+'''")) {
                    ~bought {
                        sold: ~sold {
                            price
                            quantity: count(bought)
                        }
                    }
                }
                
                response(func: has(name)){
                    name
                    providers: ~belongs {
                        sold: ~sold {
                            price
                            quantity: count(bought)
                        }
                    }
                }
            }
        '''
        return query

    @staticmethod
    def get_orders_per_location():
        return """
            {
                response(func: has(name)){
                    name
                    providers: ~belongs {
                        sold: count(~sold)
                    }
                }
            }
        """

    @staticmethod
    def get_best_sellers():
        return """
            {
                var(func: has(description)) {
                    c as count(bought) 
                }
                    
                response(func: has(description), orderdesc: val(c)){
                    description
                    times: val(c)
                    price
                }
            }
        """

    @staticmethod
    def get_worst_sales():
        return """
            {
                var(func: has(description)) {
                    c as count(bought) 
                }
                    
                response(func: has(description), orderasc: val(c)){
                    description
                    times: val(c)
                    price
                }
            }
        """

    @staticmethod
    def get_most_selled_products():
        return """
            {
                var(func: has(description)) {
                    c as count(bought) 
                }
                    
                response(func: has(description), orderdesc: val(c)){
                    description
                    times: val(c)
                }
            }
        """

    @staticmethod
    def get_most_selled_products_by_period(start_date,end_date):
        query='''
            {
                var(func: has(invoice)) @filter(ge(date, "'''+start_date+'''") AND le(date, "'''+end_date+'''")) {
                    product as ~bought
                }

                var(func: uid(product)) {
                    purchasedProduct as uid
                }

                var(func: has(description)) {
                    c as count(bought) 
                }
                
                response(func: uid(purchasedProduct), orderdesc: val(c)) @cascade {
                    description
                    times: val(c)
                }
            }
        '''
        return query
odoo.define('pos_multi_uom_product_right', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var core = require('web.core');
    var PosPopWidget = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');
    var screens = require('point_of_sale.screens');
    var QWeb = core.qweb;
    var _t = core._t;
    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var field_utils = require('web.field_utils');

    models.load_fields('product.product',['has_multi_uom','allow_uoms','show_all_uom']);

    var MulitUOMWidget = PosPopWidget.extend({
        template: 'MulitUOMWidget',

        renderElement: function(){
            var self = this;
            this._super();
            this.$(".multi_uom_button").click(function(){
                var uom_id = $(this).data('uom_id');
                var price = $(this).data('price');
                var line = self.options.selectedOrderLine;
                if(line){
                    line.set_unit_price(price);
                    line.set_product_uom(uom_id);
                }
                
                self.gui.show_screen('products');
            });
        },
        show: function(options){
            var self = this;
            this.options = options || {};
            var modifiers_list = [];
            var orderline = this.options.selectedOrderLine;
            for(var key in self.pos.units_by_id){

                if(self.pos.units_by_id[key].category_id[1]===orderline.get_unit().category_id[1]){
                    if(this.options.product.show_all_uom){
                        var price=orderline.price*orderline.get_unit().factor/self.pos.units_by_id[key].factor;
                        modifiers_list.push({id:self.pos.units_by_id[key].id,name:self.pos.units_by_id[key].display_name,price:price,factor_inv:self.pos.units_by_id[key].factor_inv});
                    }
                    else{
                        if($.inArray( self.pos.units_by_id[key].id, this.options.product.allow_uoms ) >= 0){
                            var price=orderline.price*orderline.get_unit().factor/self.pos.units_by_id[key].factor;
                            modifiers_list.push({id:self.pos.units_by_id[key].id,name:self.pos.units_by_id[key].display_name,price:price,factor_inv:self.pos.units_by_id[key].factor_inv});
                        }
                    }
                }
            }
            options.ss_uom_list = modifiers_list;
            this._super(options); 
            this.renderElement();
        },
    });

    gui.define_popup({
        'name': 'multi-uom-widget', 
        'widget': MulitUOMWidget,
    });

    screens.OrderWidget.include({
        render_orderline: function(orderline){
            var self = this;
            var el_node = this._super(orderline);
            var order = this.pos.get_order();
            $(el_node).find(".uom-button").click(function(event){
                var selectedOrderLine = order.get_orderline($(this).data('id'));
                var product = selectedOrderLine.get_product();
                if(product.has_multi_uom){
                    self.gui.show_popup('multi-uom-widget',{
                        product: product,
                        selectedOrderLine: selectedOrderLine
                    });
                }
                event.stopPropagation();
            });
            return el_node;
        },
    });

    var _super_Order = models.Order.prototype;
	models.Order = models.Order.extend({
        // override set_pricelist function to avoid recalculate when client is set
        set_pricelist: function (pricelist) {
            var self = this;
            this.pricelist = pricelist;

            var lines_to_recompute = _.filter(this.get_orderlines(), function (line) {
                return ! line.price_manually_set;
            });
            _.each(lines_to_recompute, function (line) {
                if(line.wvproduct_uom === ''){
                    line.set_unit_price(line.product.get_price(self.pricelist, line.get_quantity()));
                    self.fix_tax_included_price(line);
                }
            });
            this.trigger('change');
        },
	});

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr, options) {
            _super_orderline.initialize.call(this,attr,options);
            this.wvproduct_uom = '';
        },
        set_product_uom: function(uom_id){
            this.wvproduct_uom = this.pos.units_by_id[uom_id];
            this.trigger('change',this);
        },

        // override set_quantity function to avoid recalculate in set price by type of uom
        set_quantity: function(quantity, keep_price){

            this.order.assert_editable();
            if(quantity === 'remove'){
                this.order.remove_orderline(this);
                return;
            }else{
                var quant = parseFloat(quantity) || 0;
                var unit = this.get_unit();
                if(unit){
                    if (unit.rounding) {
                        var decimals = this.pos.dp['Product Unit of Measure'];
                        var rounding = Math.max(unit.rounding, Math.pow(10, -decimals));
                        this.quantity    = round_pr(quant, rounding);
                        this.quantityStr = field_utils.format.float(this.quantity, {digits: [69, decimals]});
                    } else {
                        this.quantity    = round_pr(quant, 1);
                        this.quantityStr = this.quantity.toFixed(0);
                    }
                }else{
                    this.quantity    = quant;
                    this.quantityStr = '' + this.quantity;
                }
            }

            // just like in sale.order changing the quantity will recompute the unit price
            if(this.wvproduct_uom === ''){
                if(! keep_price && ! this.price_manually_set){
                    this.set_unit_price(this.product.get_price(this.order.pricelist, this.get_quantity()));
                    this.order.fix_tax_included_price(this);
                }
            }
            this.trigger('change', this);
        },

        get_unit: function(){
            var unit_id = this.product.uom_id;
            if(!unit_id){
                return undefined;
            }
            unit_id = unit_id[0];
            if(!this.pos){
                return undefined;
            }
            return this.wvproduct_uom == '' ? this.pos.units_by_id[unit_id] : this.wvproduct_uom;
        },

        export_as_JSON: function(){
            var unit_id = this.product.uom_id;
            var json = _super_orderline.export_as_JSON.call(this);
            json.product_uom = this.wvproduct_uom == '' ? unit_id.id : this.wvproduct_uom.id;
            return json;
        },

        init_from_JSON: function(json){
            _super_orderline.init_from_JSON.apply(this,arguments);
            this.wvproduct_uom = json.wvproduct_uom;
        },
    });

});


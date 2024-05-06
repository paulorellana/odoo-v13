odoo.define('select_invoice_format_pos.ReceiptScreenWidget', function (require) {
    "use strict";

    var rpc = require('web.rpc');
    var screens = require('point_of_sale.screens');

    var ReceiptScreenWidget = screens.ReceiptScreenWidget;
    ReceiptScreenWidget.include({
        init: function (parent, options) {
            this._super(parent, options);
            this.report_value = false;
            this.is_rendering_report = false;
        },
        renderElement: function () {
            var self = this;
            this._super();
            this.$('.button.electronic-receipt').click(function () {
                if (!self._locked) {
                    self.print_electronic_receipt();
                }
            });
        },
        get_dynamic_report: async function (order_reference, report_id) {
            let report_value = false;
            await rpc.query({
                model: 'pos.order',
                method: 'generate_dynamic_report_pos_ui',
                args: [order_reference, report_id],
            }).then(function (data) {
                if (data['error'] === false) {
                    report_value = data['report'];
                }
            }).catch(function (error) {
                console.error(error);
            });
            return report_value;
        },
        print_electronic_receipt: async function () {
            const order = this.pos.get_order();
            if (this.is_rendering_report) {
                return;
            } else {
                this.is_rendering_report = true;
            }
            if (this.pos.config.invoice_report_id) {
                this.report_value = await this.get_dynamic_report(order.name, this.pos.config.invoice_report_id[0]);
                if (this.report_value) {
                    try {
                        // https://github.com/crabbly/Print.js/releases/
                        // https://printjs.crabbly.com/
                        printJS({
                            printable: this.report_value,
                            type: 'pdf',
                            base64: true,
                            showModal: true
                        });
                    } catch (e) {
                        console.error(e);
                    }
                }
            }
            this.report_value = false;
            this.is_rendering_report = false;
        },
        handle_auto_print: function () {
            if (this.pos.config.automatic_print_electronic_invoice) {
                this.print_electronic_receipt();
            } else {
                if (this.should_auto_print() && !this.pos.get_order().is_to_email()) {
                    this.print();
                    if (this.should_close_immediately()) {
                        this.click_next();
                    }
                } else {
                    this.lock_screen(false);
                }
            }
        },
    });
});

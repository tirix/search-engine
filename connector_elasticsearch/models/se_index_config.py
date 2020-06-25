# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class SeIndexConfig(models.Model):

    _name = "se.index.config"
    _description = "Elasticsearch index configuration"

    name = fields.Char(required=True)
    body = fields.Serialized(required=True)
    # This field is used since no widget exists to edit a serialized field
    # into the web fontend
    body_str = fields.Text(compute="_compute_body_str", inverse="_inverse_body_str")

    @api.model
    def create(self, values):
        # For new record creation, the inverse function for `body_str` is 
        # called after the record is inserted into database. The field 
        # `body` would be empty, and a validation error will pop up as field 
        # `body` is required. The solution is to override create function, 
        # and initialize field `body` based on field `body_str`.
        if 'body' not in values and 'body_str' in values:
            values['body'] = json.loads(values['body_str'])

        return super(SeIndexConfig, self).create(values)

    @api.multi
    @api.depends("body")
    def _compute_body_str(self):
        for rec in self:
            if rec.body:
                rec.body_str = json.dumps(rec.body)

    @api.multi
    def _inverse_body_str(self):
        for rec in self:
            data = None
            if rec.body_str:
                data = json.loads(rec.body_str)
            rec.body = data

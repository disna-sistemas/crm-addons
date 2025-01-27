# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _
from odoo.exceptions import ValidationError


class CrmLead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    @api.model
    def default_get(self, fields):
        result = super(CrmLead2OpportunityPartner, self).default_get(fields)
        if self._context.get('active_id'):
            lead = self.env['crm.lead'].browse(self._context['active_id'])
            if not lead.future_student_ids:
                raise ValidationError(
                    _('There must be at least one future student.'))
        return result

    @api.multi
    def action_apply(self):
        lead_obj = self.env['crm.lead']
        if self.name != 'merge':
            for lead in lead_obj.browse(self._context.get('active_ids', [])):
                if not lead.future_student_ids:
                    raise ValidationError(
                        _('You must define a future student in the lead: {}.'
                          ).format(lead.name))
        return super(CrmLead2OpportunityPartner, self).action_apply()

    @api.onchange('team_id')
    def _onchange_team_id(self):
        if self.team_id and self.team_id.user_id:
            self.user_id = self.team_id.user_id

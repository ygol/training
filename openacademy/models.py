# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'

#     name = fields.Char()

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one(
        'res.users', ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)

    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|', ('instructor', '=', True),('category_id.name', 'ilike', "Teacher")])

    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string='Course', required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    total_qty = fields.Integer(string=None, compute='_total_qty')

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        print "before test"
        # import ipdp; ipdb.set_trace()
        if not self.seats:
            print "first if"
            self.taken_seats = 0.0
        else:
            print "second cond else"
            self.taken_seats = 100.0 * len(self.attendee_ids) / self.seats

    def _total_qty(self):
        #sum of line's quantities
        total = 0
        #import ipdb;ipdb.set_trace()
        for attendee_id in self.attendee_ids:
            total = total + attendee_id.qty

        self.total_qty = total

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negtive",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }


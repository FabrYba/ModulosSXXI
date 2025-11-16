from io import BytesIO

from odoo import fields, http
from odoo.http import request, content_disposition
from odoo.service import db as db_service


class BackupManagerController(http.Controller):

    @http.route("/backup_manager/download", type="http", auth="user")
    def backup_manager_download(self, **kwargs):
        if not request.env.user.has_group("db_backup_demo.group_backup_manager"):
            return request.not_found()

        db_name = request.env.cr.dbname
        backup_format = "zip"

        stream = BytesIO()
        db_service.dump_db(db_name, stream, backup_format)
        stream.seek(0)

        filename = "%s-%s.%s" % (db_name, fields.Date.today(), backup_format)

        return request.make_response(
            stream.read(),
            headers=[
                ("Content-Type", "application/zip"),
                ("Content-Disposition", content_disposition(filename)),
            ],
        )

from marshmallow import Schema, fields, validate
from app.schema.address_schema import AddressSchema
from app.schema.roles_schema import RolesSchema

class UserSchema(Schema):
    class Meta:
        model = ('id_user', 'name', 'username', 'email', 'password')

    id_user = fields.UUID(dump_only=True)
    name = fields.Str(required=True,
                      validate=[
                          validate.Length(min=2, max=100),
                          validate.Regexp(r'^[a-zA-Z\s]+$',
                                          error='Invalid name format, Only letters and space are allowed.')
                      ])
    username = fields.Str(required=True,
                          validate=[
                              validate.Length(min=4, max=12,
                                              error='Username must be between 4 and 12 characters.')
                          ])
    email = fields.Email(required=True,
                         validate=validate.Email(error='Invalid email format'))
    password = fields.Str(required=True,
                          validate=[
                              validate.Length(min=8),
                              validate.Regexp(
                                  r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).*$',
                                  error='Password must containat least one lowercase letter, one uppercase latter, one digit, and one special character.'
                              )
                          ])
    picture = fields.Str(validate=validate.Length(max=200))
    is_active = fields.Boolean()
    phone_number = fields.Str(
        validate=[
            validate.Regexp(
                r'^\+?[1-9]\d{1,14}$',
                error='Invalid phone number format. It should start with "+" (optional) followed by digits (1-14 digits allowed).'
            )
        ]
    )
    id_address = fields.Nested(AddressSchema, attribute='tbl_address', many=False)
    id_role = fields.Nested(RolesSchema, attribute='tbl_roles', many=False)
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

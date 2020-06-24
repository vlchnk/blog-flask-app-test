from os.path import dirname, join

from flask import Flask, g

from . import auth, blog, db

app = Flask( __name__ )
app.config.from_mapping(
    SECRET_KEY='00i0T_6qs7UnaSO246RF2NqTB_ztf2342asfasSYdas^&21',
    OIDC_CLIENT_SECRETS=join(dirname(dirname( __file__ )), "client_secrets.json"),
    OIDC_COOKIE_SECURE=False,
    OIDC_CALLBACK_ROUTE="/oidc/callback",
    OIDC_SCOPES=["openid", "email", "profile"],
    OIDC_ID_TOKEN_COOKIE_NAME="oidc_token",
    SQLALCHEMY_DATABASE_URI="sqlite:///" + join(dirname(dirname( __file__ )), "database.sqlite"),
)

auth.oidc.init_app(app)
db.init_app(app)

app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)

@app.before_request
def before_request():
    """
    Load a user object into `g.user` before each request.
    """
    if auth.oidc.user_loggedin:
        g.user = auth.okta_client.get_user(auth.oidc.user_getfield("sub"))
    else:
        g.user = None

# @app.errorhandler(404)
# def page_not_found(e):
#     """Render a 404 page."""
#     return render_template("404.html"), 404

# @app.errorhandler(403)
# def insufficient_permissions(e):
#     """Render a 403 page."""
#     return render_template("403.html"), 403

import pytest
from scripts.script_helpers.render_template_helpers import render_nginx_template

DUMMY_ENV_VARS = [
    ("DM_RESOLVER_IP", "172.0.0.0"),
    ("DM_CLOUDFRONT_IPS", "172.0.0.0,172.0.0.1"),
    ("DM_USER_IPS", "172.0.0.2,172.1.1.2"),
    ("DM_DEV_USER_IPS", "172.0.0.3,172.1.1.3"),
    ("DM_ADMIN_USER_IPS", "172.0.0.4,172.1.1.4"),
    ("DM_FRONTEND_URL", "http://example.net"),
    ("DM_API_URL", "http://localhost:5000"),
    ("DM_SEARCH_API_URL", "http://localhost:5009"),
    ("DM_ANTIVIRUS_API_URL", "http://localhost:5008"),
    ("DM_APP_AUTH", "12345678"),
    ("DM_DOCUMENTS_S3_URL", "https://example1.com"),
    ("DM_G7_DRAFT_DOCUMENTS_S3_URL", "https://example2.com"),
    ("DM_AGREEMENTS_S3_URL", "https://example3.com"),
    ("DM_COMMUNICATIONS_S3_URL", "https://example4.com"),
    ("DM_REPORTS_S3_URL", "https://example5.com"),
    ("DM_SUBMISSIONS_S3_URL", "https://example6.com"),
    ("DM_RATE_LIMITING_ENABLED", "enabled")
]


@pytest.fixture
def setup_env(monkeypatch):
    for env_var, val in DUMMY_ENV_VARS:
        monkeypatch.setenv(env_var, val)


class TestRenderNginxTemplates:

    def test_render_nginx_template_with_no_env_vars_raises_value_error(self):
        with pytest.raises(ValueError) as exc:
            render_nginx_template("templates/api.j2")
        assert "Variable 'resolver_ip' is undefined" in str(exc.value)

    def test_render_nginx_template_api(self, setup_env):
        api_template = render_nginx_template("templates/api.j2")
        assert "server_name api.*" in api_template
        # Check env vars
        assert "set $api_url http://localhost:5000;" in api_template
        assert "set $antivirus_api_url http://localhost:5008;" in api_template
        assert "set $search_api_url http://localhost:5009;" in api_template
        assert "resolver 172.0.0.0 valid=10s;" in api_template
        # dev user IPs
        assert "allow 172.0.0.3" in api_template
        assert "allow 172.1.1.3" in api_template

    def test_render_nginx_template_assets(self, setup_env):
        assets_template = render_nginx_template("templates/assets.j2")
        assert "server_name assets.*" in assets_template
        # Check env vars
        assert "set $g7_draft_documents_s3_url https://example2.com;" in assets_template
        assert "set $frontend_url http://example.net;" in assets_template
        assert "set $documents_s3_url https://example1.com;" in assets_template
        assert "set $agreements_s3_url https://example3.com;" in assets_template
        assert "set $communications_s3_url https://example4.com;" in assets_template
        assert "set $submissions_s3_url https://example6.com;" in assets_template
        assert "set $reports_s3_url https://example5.com;" in assets_template

    def test_render_nginx_template_healthcheck(self):
        healthcheck_template = render_nginx_template("templates/healthcheck.j2")
        assert "location /_status" in healthcheck_template

    def test_render_nginx_template_maintenance(self, setup_env):
        maintenance = render_nginx_template("templates/maintenance.j2")
        assert "server_name www.*" in maintenance
        assert "error_page 503 @maintenance;" in maintenance
        # Check user_ips list has been included
        assert "allow 172.0.0.2" in maintenance
        assert "allow 172.1.1.2" in maintenance

    def test_render_nginx_template_metrics(self, setup_env):
        metrics_template = render_nginx_template("templates/metrics.j2")
        assert "server_name *.cloudapps.digital" in metrics_template
        assert "location /_metrics" in metrics_template
        assert "location /stub-status" in metrics_template

    def test_render_nginx_template_nginx_conf_rate_limiting_enabled(self, setup_env):
        nginx_conf_template = render_nginx_template("templates/nginx.conf.j2")
        assert "resolver 172.0.0.0 valid=300s;" in nginx_conf_template
        assert "set_real_ip_from 172.0.0.0" in nginx_conf_template
        assert "set_real_ip_from 172.0.0.1" in nginx_conf_template
        assert "limit_req_status 429;" in nginx_conf_template

    def test_render_nginx_template_nginx_conf_rate_limiting_disabled(self, setup_env, monkeypatch):
        monkeypatch.setenv("DM_RATE_LIMITING_ENABLED", "disabled")

        nginx_conf_template = render_nginx_template("templates/nginx.conf.j2")
        assert "limit_req_status 429;" not in nginx_conf_template

    def test_render_nginx_template_www_rate_limiting_enabled(self, setup_env, monkeypatch):
        www_template = render_nginx_template("templates/www.j2")
        assert "server_name www.*" in www_template
        assert 'proxy_set_header Authorization "Basic 12345678";' in www_template
        # Rate limiting
        assert "error_page 429 @too_many_requests;" in www_template
        assert "# Listen on port 10823 and serve a static_429_error page" in www_template
        # Admin IPs
        assert "allow 172.0.0.4;" in www_template
        assert "allow 172.1.1.4;" in www_template

    def test_render_nginx_template_www_rate_limiting_disabled(self, setup_env, monkeypatch):
        monkeypatch.setenv("DM_RATE_LIMITING_ENABLED", "disabled")

        www_template = render_nginx_template("templates/www.j2")
        assert "error_page 429 @too_many_requests;" not in www_template
        assert "# Listen on port 10823 and serve a static_429_error page" not in www_template

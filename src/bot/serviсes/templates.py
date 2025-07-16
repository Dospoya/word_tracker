import jinja2


def get_template_renderer(
    template_dir: str,
):
    templates = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
    )

    def render_template(template_name: str, **kwargs):
        template = templates.get_template(template_name)
        return template.render(**kwargs)

    return render_template


render_template = get_template_renderer("src/bot/templates")

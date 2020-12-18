from flask_assets import Bundle


def compile_static_assets(assets):
    """
    Compile stylesheets if in development mode.

    :param assets: Flask-Assets Environment
    :type assets: Environment
    """
    assets.auto_build = True
    assets.debug = False
    main_less_bundle = Bundle(
        'less/main/*.less',
        filters='less,cssmin',
        output='dist/css/styles.css',
        extra={'rel': 'stylesheet/less'}
    )

    assets.register('less_main', main_less_bundle)

    main_less_bundle.build()
    return assets

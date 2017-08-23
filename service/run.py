from flask_failsafe import failsafe

@failsafe
def create_app():
    from service.app import manager
    return manager

def cli_entry():
    create_app().run()

if __name__ == '__main__':
    create_app().run()

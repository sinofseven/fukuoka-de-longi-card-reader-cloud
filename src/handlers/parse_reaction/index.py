from jeffy.framework import Jeffy

app = Jeffy()


@app.decorator.auto_logging
def handler(event, context):
    main(event)


def main(event):
    pass

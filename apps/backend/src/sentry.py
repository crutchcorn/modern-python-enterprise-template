import sentry_sdk

sentry_sdk.init(
    dsn="https://ff8e0dd3d1e24043e35ee98e9847571a@o4511216682795008.ingest.us.sentry.io/4511216684498944",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

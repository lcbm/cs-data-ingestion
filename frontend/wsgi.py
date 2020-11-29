"""Application entry point."""

import frontend


app = frontend.create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")

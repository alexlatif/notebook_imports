def init():
    ! pip install pandas
    ! pip install numpy
    ! pip install pydantic
    ! pip install IPython
    ! pip install tensorflow-macos # TODO will have to change this
    ! pip install tensorflow-cloud
    ! pip install grpcio-status==1.48.2 
    ! pip install --upgrade google-cloud-aiplatform google-cloud-storage google-cloud-bigquery pyarrow
    ! pip install Pyarrow
    ! pip uninstall -y mvc
    ! pip install git+https://github.com/alexlatif/mvc.git
    ! pip install db_dtypes
    ! pip install fsspec
    ! pip install gcsfs

    import os
    import IPython
    import sys
    import os
    import pandas as pd
    import numpy as np
    import datetime
    import typing
    from pydantic import BaseModel

    if "google.colab" not in sys.modules:
        sys.path.append(
            ".."
        )

    import platform
    from distutils import util

    if 'arm64' in platform.machine() and 'mac' in util.get_platform():
        os.environ["GRPC_PYTHON_BUILD_SYSTEM_OPENSSL"] = "1"
        os.environ["GRPC_PYTHON_BUILD_SYSTEM_ZLIB"] = "1"
    else:
        pass 

    # The Vertex AI Workbench Notebook product has specific requirements
    IS_WORKBENCH_NOTEBOOK = os.getenv("DL_ANACONDA_HOME")
    IS_USER_MANAGED_WORKBENCH_NOTEBOOK = os.path.exists(
        "/opt/deeplearning/metadata/env_version"
    )

    # Vertex AI Notebook requires dependencies to be installed with '--user'
    USER_FLAG = ""
    if IS_WORKBENCH_NOTEBOOK:
        USER_FLAG = "--user"

    # If on Vertex AI Workbench, then don't execute this code
    IS_COLAB = "google.colab" in sys.modules
    if not os.path.exists("/opt/deeplearning/metadata/env_version") and not os.getenv(
        "DL_ANACONDA_HOME"
    ):
        if "google.colab" in sys.modules:
            from google.colab import auth as google_auth, drive 

            print("must restart kernal")
            app = IPython.Application.instance()
            app.kernel.do_shutdown(True)

            print("LOGIN TO DRIVE TO ACCESS SHARED KEYS")
            drive.mount('/content/drive')
            print("gdrive mounted!")

            config_file = "ml-wtz.json"
            shared_dir = f"{UNIQUE_DRIVE_DIR}/{config_file}" # chang this as the top of file 
            local_dir = f"drive/MyDrive/ml/ml_shared_config/{config_file}" # change this only if sharing config file

            if os.path.exists(shared_dir): 
                print("USING SHARED DRIVE CONFIG")
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = shared_dir
            elif os.path.exists(local_dir):
                print("USING USER LOCAL CONFIG")
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = local_dir

            # ! pip install --upgrade google-cloud-aiplatform google-cloud-storage google-cloud-bigquery pyarrow $USER_FLAG -q
            ! pip install tensorflow-hub $USER_FLAG -q

            # TODO workbench specific
            # print("auth google user")
            # google_auth.authenticate_user()

    local_file_path = r'dev_utils/ml_wtz_gcp_config.json' # if config file is local

    if os.path.exists(local_file_path):
        print("USING LOCAL CONFIG")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = local_file_path
    else:
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise Exception("no GOOGLE_APPLICATION_CREDENTIALS set")


    os.environ["PROJECT_ID"] = "ml-wtz"
    os.environ["REGION"] = "us-east1"
    os.environ["DEPLOY_COMPUTE"] = "n1-standard-2"
    os.environ["MODEL_PREDICT_CONTAINER_URI"]  = "us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-11:latest"
    os.environ["SERVICES_CONFIGED"] = ",".join(["workout_decisions", "lstm_options"])

    from google.cloud import bigquery, storage
    from google.cloud import aiplatform
    import tensorflow as tf
    import tensorflow_cloud as tfc
    import mvc as model_version_controller
    mvc = model_version_controller.ModelVersionController()
import os

STAGE = os.getenv("STAGE", "dev")
TRANSCRIPTS_BUCKET = os.getenv("TRANSCRIPTS_BUCKET", "osiris-transcripts-staging")

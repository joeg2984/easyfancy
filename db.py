from sqlmodel import create_engine, SQLModel, Session

def init_db():
    SQLModel.metadata.create_all(engine)

DATABASE_URL = 'postgresql+psycopg://postgres.llrfqpkbojsczfpiivqz:dysdi4-xebDud-zigsaq@aws-0-us-east-1.pooler.supabase.com:6543/postgres'

# Consider using environment variables for sensitive credentials
engine = create_engine(DATABASE_URL, echo=True)

# Get session for use in scripts or simple context
def get_session():
    with Session(engine) as session:
        yield session
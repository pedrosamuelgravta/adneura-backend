from alembic import op
import sqlalchemy as sa

revision = "994a22f453f3"
down_revision = "8786bc693848"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Aplica a alteração que faltou na migration anterior
    op.add_column(
        "strategic_goals", sa.Column("campaign_id", sa.Uuid(), nullable=False)
    )
    op.drop_constraint(
        "strategic_goals_brand_id_fkey", "strategic_goals", type_="foreignkey"
    )
    op.create_foreign_key(None, "strategic_goals", "campaigns", ["campaign_id"], ["id"])
    op.drop_column("strategic_goals", "brand_id")


def downgrade() -> None:
    # Restaura o estado anterior
    op.add_column(
        "strategic_goals",
        sa.Column("brand_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "strategic_goals", type_="foreignkey")
    op.create_foreign_key(
        "strategic_goals_brand_id_fkey",
        "strategic_goals",
        "brands",
        ["brand_id"],
        ["id"],
    )
    op.drop_column("strategic_goals", "campaign_id")

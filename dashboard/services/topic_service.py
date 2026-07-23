from sqlalchemy.orm import Session

from app.database.repositories.topic_repository import (
    TopicRepository,
)


class DashboardTopicService:

    def __init__(self, db: Session):

        self.repo = TopicRepository(db)

    # =====================================================
    # GET TOPICS
    # =====================================================

    def get_topics(

        self,

        keyword=None,

        category=None,

        page=1,

        per_page=20,

    ):

        return self.repo.search(

            keyword=keyword,

            category=category,

            page=page,

            per_page=per_page,

        )

    # =====================================================
    # TOTAL
    # =====================================================

    def total_topics(

        self,

        keyword=None,

        category=None,

    ):

        return self.repo.count(

            keyword=keyword,

            category=category,

        )

    # =====================================================
    # CATEGORY
    # =====================================================

    def get_categories(self):

        return self.repo.categories()

    # =====================================================
    # CHART
    # =====================================================

    def get_chart_data(

        self,

        keyword=None,

        category=None,

    ):

        return self.repo.get_all(

            keyword=keyword,

            category=category,

        )
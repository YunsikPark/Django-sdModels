from datetime import datetime

from django.db import models
from django.db.models import Q


class Player(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


    @property
    def current_club(self):
        return self.current_tradeinfo.club


    @property
    def current_tradeinfo(self):
        return self.tradeinfo_set.get(date_leaved__isnull=True)

        # current_club 프로퍼티에 현재 속하는 Club 리턴


        # current_tradeinfo 프로퍼티에 현재 자신의 TradeInfo 리턴


class Club(models.Model):
    name = models.CharField(max_length=40)
    players = models.ManyToManyField(
        Player,
        through='TradeInfo',
        through_fields=('club', 'player'),
    )

    def __str__(self):
        return self.name

    def squad(self, year=None):
        if year:
            print(datetime(year + 1, 1, 1))
            return self.players.filter(
               Q(tradeinfo__date_joined__lt=datetime(year+1,1,1)) &
                (
                    Q(otradeinfo__date_leaved__gt=datetime(year+1,1)) |
                    Q(tradeinfo__date_leaved_isnull=True)
                ),
            )
        else:
            # squad 메서드에 현직 선수들만 리턴
            return self.players.filter(tradeinfo__date_leaved__isnull=True)

        # 인수로 년도(2017,2015...등)를 받아
        # 해당 년도의 현직 선수들을 리턴,
        # 주어지지 않으면 현재를 기준으로 함


class TradeInfo(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    date_joined = models.DateField()
    date_leaved = models.DateField(null=True, blank=True)
    recommender = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name='tradeinfo_set_by_recommender',
        null=True,
        blank=True
    )
    prev_club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name='+',
        null=True,
        blank=True
    )

    # 1. property로 is_current 속성이 TradeInfo가 현재 현직(leaved하지 않았는지)여부 반환
    # 2. recommender와 prev_club을 활성화 시키고 Club의 MTM필드에 through_fields를 명시

    def __str__(self):
        # 선수이름, 구단명(시작일자 ~ 종료일자)
        # date_leaved가 None일경우 '현직'을 출력하도록 함
        return '{}, {} ({} ~ {})'.format(
            self.player.name,
            self.club.name,
            self.date_joined,
            self.date_leaved or '현직'
            # self.date_leaved if self.date_leaved else '현직'
        )

    @property
    def is_current(self):
        return self.date_leaved is None

        # 위의 요구조건들을 만족하는 실행코드 작성

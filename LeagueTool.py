import time
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger, JSON, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

Base = declarative_base()

# ── Entities ──────────────────────────────────────────────────────────────────

class AccountDto(Base):
    __tablename__ = 'account'
    id    = Column(Integer, primary_key=True, autoincrement=True)
    puuid = Column(String)

class MatchIdDto(Base):
    __tablename__ = 'match_id'
    id      = Column(Integer, primary_key=True, autoincrement=True)
    puuid   = Column(String)
    matchId = Column(String)

class MatchMetadataDto(Base):
    __tablename__ = 'match_metadata'
    id           = Column(Integer, primary_key=True, autoincrement=True)
    dataVersion  = Column(String)
    matchId      = Column(String)
    participants = Column(JSON)

class MatchInfoDto(Base):
    __tablename__ = 'match_info'
    id                 = Column(Integer, primary_key=True, autoincrement=True)
    endOfGameResult    = Column(String)
    gameCreation       = Column(BigInteger)
    gameDuration       = Column(BigInteger)
    gameEndTimestamp   = Column(BigInteger)
    gameId             = Column(BigInteger)
    gameMode           = Column(String)
    gameName           = Column(String)
    gameStartTimestamp = Column(BigInteger)
    gameType           = Column(String)
    gameVersion        = Column(String)
    mapId              = Column(Integer)
    platformId         = Column(String)
    queueId            = Column(Integer)
    tournamentCode     = Column(String)
    participants = relationship('ParticipantDto', back_populates='info')
    teams        = relationship('TeamDto',        back_populates='info')

class ParticipantDto(Base):
    __tablename__ = 'match_participant'
    id                             = Column(Integer, primary_key=True, autoincrement=True)
    info_id                        = Column(Integer, ForeignKey('match_info.id'))
    allInPings                     = Column(Integer)
    assistMePings                  = Column(Integer)
    assists                        = Column(Integer)
    baronKills                     = Column(Integer)
    bountyLevel                    = Column(Integer)
    champExperience                = Column(Integer)
    champLevel                     = Column(Integer)
    championId                     = Column(Integer)
    championName                   = Column(String)
    commandPings                   = Column(Integer)
    championTransform              = Column(Integer)
    consumablesPurchased           = Column(Integer)
    damageDealtToBuildings         = Column(Integer)
    damageDealtToObjectives        = Column(Integer)
    damageDealtToTurrets           = Column(Integer)
    damageSelfMitigated            = Column(Integer)
    deaths                         = Column(Integer)
    detectorWardsPlaced            = Column(Integer)
    doubleKills                    = Column(Integer)
    dragonKills                    = Column(Integer)
    eligibleForProgression         = Column(Boolean)
    enemyMissingPings              = Column(Integer)
    enemyVisionPings               = Column(Integer)
    firstBloodAssist               = Column(Boolean)
    firstBloodKill                 = Column(Boolean)
    firstTowerAssist               = Column(Boolean)
    firstTowerKill                 = Column(Boolean)
    gameEndedInEarlySurrender      = Column(Boolean)
    gameEndedInSurrender           = Column(Boolean)
    holdPings                      = Column(Integer)
    getBackPings                   = Column(Integer)
    goldEarned                     = Column(Integer)
    goldSpent                      = Column(Integer)
    individualPosition             = Column(String)
    inhibitorKills                 = Column(Integer)
    inhibitorTakedowns             = Column(Integer)
    inhibitorsLost                 = Column(Integer)
    item0                          = Column(Integer)
    item1                          = Column(Integer)
    item2                          = Column(Integer)
    item3                          = Column(Integer)
    item4                          = Column(Integer)
    item5                          = Column(Integer)
    item6                          = Column(Integer)
    itemsPurchased                 = Column(Integer)
    killingSprees                  = Column(Integer)
    kills                          = Column(Integer)
    lane                           = Column(String)
    largestCriticalStrike          = Column(Integer)
    largestKillingSpree            = Column(Integer)
    largestMultiKill               = Column(Integer)
    longestTimeSpentLiving         = Column(Integer)
    magicDamageDealt               = Column(Integer)
    magicDamageDealtToChampions    = Column(Integer)
    magicDamageTaken               = Column(Integer)
    needVisionPings                = Column(Integer)
    neutralMinionsKilled           = Column(Integer)
    nexusKills                     = Column(Integer)
    nexusTakedowns                 = Column(Integer)
    nexusLost                      = Column(Integer)
    objectivesStolen               = Column(Integer)
    objectivesStolenAssists        = Column(Integer)
    onMyWayPings                   = Column(Integer)
    participantId                  = Column(Integer)
    pentaKills                     = Column(Integer)
    physicalDamageDealt            = Column(Integer)
    physicalDamageDealtToChampions = Column(Integer)
    physicalDamageTaken            = Column(Integer)
    placement                      = Column(Integer)
    playerAugment1                 = Column(Integer)
    playerAugment2                 = Column(Integer)
    playerAugment3                 = Column(Integer)
    playerAugment4                 = Column(Integer)
    playerSubteamId                = Column(Integer)
    pushPings                      = Column(Integer)
    profileIcon                    = Column(Integer)
    puuid                          = Column(String)
    quadraKills                    = Column(Integer)
    riotIdGameName                 = Column(String)
    riotIdTagline                  = Column(String)
    role                           = Column(String)
    sightWardsBoughtInGame         = Column(Integer)
    spell1Casts                    = Column(Integer)
    spell2Casts                    = Column(Integer)
    spell3Casts                    = Column(Integer)
    spell4Casts                    = Column(Integer)
    subteamPlacement               = Column(Integer)
    summoner1Casts                 = Column(Integer)
    summoner1Id                    = Column(Integer)
    summoner2Casts                 = Column(Integer)
    summoner2Id                    = Column(Integer)
    summonerId                     = Column(String)
    summonerLevel                  = Column(Integer)
    summonerName                   = Column(String)
    teamEarlySurrendered           = Column(Boolean)
    teamId                         = Column(Integer)
    teamPosition                   = Column(String)
    timeCCingOthers                = Column(Integer)
    timePlayed                     = Column(Integer)
    totalAllyJungleMinionsKilled   = Column(Integer)
    totalDamageDealt               = Column(Integer)
    totalDamageDealtToChampions    = Column(Integer)
    totalDamageShieldedOnTeammates = Column(Integer)
    totalDamageTaken               = Column(Integer)
    totalEnemyJungleMinionsKilled  = Column(Integer)
    totalHeal                      = Column(Integer)
    totalHealsOnTeammates          = Column(Integer)
    totalMinionsKilled             = Column(Integer)
    totalTimeCCDealt               = Column(Integer)
    totalTimeSpentDead             = Column(Integer)
    totalUnitsHealed               = Column(Integer)
    tripleKills                    = Column(Integer)
    trueDamageDealt                = Column(Integer)
    trueDamageDealtToChampions     = Column(Integer)
    trueDamageTaken                = Column(Integer)
    turretKills                    = Column(Integer)
    turretTakedowns                = Column(Integer)
    turretsLost                    = Column(Integer)
    unrealKills                    = Column(Integer)
    visionScore                    = Column(Integer)
    visionClearedPings             = Column(Integer)
    visionWardsBoughtInGame        = Column(Integer)
    wardsKilled                    = Column(Integer)
    wardsPlaced                    = Column(Integer)
    win                            = Column(Boolean)
    info = relationship('MatchInfoDto', back_populates='participants')

class TeamDto(Base):
    __tablename__ = 'match_team'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    info_id       = Column(Integer, ForeignKey('match_info.id'))
    objectives_id = Column(Integer, ForeignKey('match_objectives.id'))
    teamId        = Column(Integer)
    win           = Column(Boolean)
    info       = relationship('MatchInfoDto',  back_populates='teams')
    bans       = relationship('BanDto',        back_populates='team')
    objectives = relationship('ObjectivesDto', back_populates='team', uselist=False)

class BanDto(Base):
    __tablename__ = 'match_ban'
    id         = Column(Integer, primary_key=True, autoincrement=True)
    team_id    = Column(Integer, ForeignKey('match_team.id'))
    championId = Column(Integer)
    pickTurn   = Column(Integer)
    team = relationship('TeamDto', back_populates='bans')

class ObjectivesDto(Base):
    __tablename__ = 'match_objectives'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    baron_id      = Column(Integer, ForeignKey('match_objective.id'))
    champion_id   = Column(Integer, ForeignKey('match_objective.id'))
    dragon_id     = Column(Integer, ForeignKey('match_objective.id'))
    horde_id      = Column(Integer, ForeignKey('match_objective.id'))
    inhibitor_id  = Column(Integer, ForeignKey('match_objective.id'))
    riftHerald_id = Column(Integer, ForeignKey('match_objective.id'))
    tower_id      = Column(Integer, ForeignKey('match_objective.id'))
    team       = relationship('TeamDto',      back_populates='objectives', uselist=False)
    baron      = relationship('ObjectiveDto', foreign_keys=[baron_id])
    champion   = relationship('ObjectiveDto', foreign_keys=[champion_id])
    dragon     = relationship('ObjectiveDto', foreign_keys=[dragon_id])
    horde      = relationship('ObjectiveDto', foreign_keys=[horde_id])
    inhibitor  = relationship('ObjectiveDto', foreign_keys=[inhibitor_id])
    riftHerald = relationship('ObjectiveDto', foreign_keys=[riftHerald_id])
    tower      = relationship('ObjectiveDto', foreign_keys=[tower_id])

class ObjectiveDto(Base):
    __tablename__ = 'match_objective'
    id    = Column(Integer, primary_key=True, autoincrement=True)
    first = Column(Boolean)
    kills = Column(Integer)

class TimelineDto(Base):
    __tablename__ = 'timeline'
    id      = Column(Integer, primary_key=True, autoincrement=True)
    meta_id = Column(Integer, ForeignKey('metadata_timeline.id'))
    info_id = Column(Integer, ForeignKey('info_timeline.id'))
    meta = relationship('MetadataTimeLineDto', back_populates='timeline', uselist=False)
    info = relationship('InfoTimeLineDto',     back_populates='timeline', uselist=False)

class MetadataTimeLineDto(Base):
    __tablename__ = 'metadata_timeline'
    id           = Column(Integer, primary_key=True, autoincrement=True)
    dataVersion  = Column(String)
    matchId      = Column(String)
    participants = Column(JSON)
    timeline = relationship('TimelineDto', back_populates='meta', uselist=False)

class InfoTimeLineDto(Base):
    __tablename__ = 'info_timeline'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    endOfGameResult = Column(String)
    frameInterval   = Column(BigInteger)
    gameId          = Column(BigInteger)
    timeline     = relationship('TimelineDto',            back_populates='info', uselist=False)
    participants = relationship('ParticipantTimeLineDto', back_populates='info')
    frames       = relationship('FramesTimeLineDto',      back_populates='info')

class ParticipantTimeLineDto(Base):
    __tablename__ = 'participant_timeline'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    info_id       = Column(Integer, ForeignKey('info_timeline.id'))
    participantId = Column(Integer)
    puuid         = Column(String)
    info = relationship('InfoTimeLineDto', back_populates='participants')

class FramesTimeLineDto(Base):
    __tablename__ = 'frames_timeline'
    id        = Column(Integer, primary_key=True, autoincrement=True)
    info_id   = Column(Integer, ForeignKey('info_timeline.id'))
    timestamp = Column(Integer)
    info               = relationship('InfoTimeLineDto',      back_populates='frames')
    events             = relationship('EventsTimeLineDto',    back_populates='frame')
    participant_frames = relationship('ParticipantFramesDto', back_populates='frame', uselist=False)

class EventsTimeLineDto(Base):
    __tablename__ = 'events_timeline'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    frame_id      = Column(Integer, ForeignKey('frames_timeline.id'))
    timestamp     = Column(BigInteger)
    realTimestamp = Column(BigInteger)
    type          = Column(String)
    frame = relationship('FramesTimeLineDto', back_populates='events')

class ParticipantFramesDto(Base):
    __tablename__ = 'participant_frames'
    id       = Column(Integer, primary_key=True, autoincrement=True)
    frame_id = Column(Integer, ForeignKey('frames_timeline.id'))
    frame            = relationship('FramesTimeLineDto',   back_populates='participant_frames')
    participant_data = relationship('ParticipantFrameDto', back_populates='participant_frames')

class ParticipantFrameDto(Base):
    __tablename__ = 'participant_frame'
    id                       = Column(Integer, primary_key=True, autoincrement=True)
    participant_frames_id    = Column(Integer, ForeignKey('participant_frames.id'))
    champion_stats_id        = Column(Integer, ForeignKey('champion_stats.id'))
    damage_stats_id          = Column(Integer, ForeignKey('damage_stats.id'))
    position_id              = Column(Integer, ForeignKey('position.id'))
    currentGold              = Column(Integer)
    goldPerSecond            = Column(Integer)
    jungleMinionsKilled      = Column(Integer)
    level                    = Column(Integer)
    minionsKilled            = Column(Integer)
    participantId            = Column(Integer)
    timeEnemySpentControlled = Column(Integer)
    totalGold                = Column(Integer)
    xp                       = Column(Integer)
    participant_frames = relationship('ParticipantFramesDto', back_populates='participant_data')
    champion_stats     = relationship('ChampionStatsDto',     back_populates='participant_frame', uselist=False)
    damage_stats       = relationship('DamageStatsDto',       back_populates='participant_frame', uselist=False)
    position           = relationship('PositionDto',          back_populates='participant_frame', uselist=False)

class ChampionStatsDto(Base):
    __tablename__ = 'champion_stats'
    id                   = Column(Integer, primary_key=True, autoincrement=True)
    abilityHaste         = Column(Integer)
    abilityPower         = Column(Integer)
    armor                = Column(Integer)
    armorPen             = Column(Integer)
    armorPenPercent      = Column(Integer)
    attackDamage         = Column(Integer)
    attackSpeed          = Column(Integer)
    bonusArmorPenPercent = Column(Integer)
    bonusMagicPenPercent = Column(Integer)
    ccReduction          = Column(Integer)
    cooldownReduction    = Column(Integer)
    health               = Column(Integer)
    healthMax            = Column(Integer)
    healthRegen          = Column(Integer)
    lifesteal            = Column(Integer)
    magicPen             = Column(Integer)
    magicPenPercent      = Column(Integer)
    magicResist          = Column(Integer)
    movementSpeed        = Column(Integer)
    omnivamp             = Column(Integer)
    physicalVamp         = Column(Integer)
    power                = Column(Integer)
    powerMax             = Column(Integer)
    powerRegen           = Column(Integer)
    spellVamp            = Column(Integer)
    participant_frame = relationship('ParticipantFrameDto', back_populates='champion_stats', uselist=False)

class DamageStatsDto(Base):
    __tablename__ = 'damage_stats'
    id                            = Column(Integer, primary_key=True, autoincrement=True)
    magicDamageDone               = Column(Integer)
    magicDamageDoneToChampions    = Column(Integer)
    magicDamageTaken              = Column(Integer)
    physicalDamageDone            = Column(Integer)
    physicalDamageDoneToChampions = Column(Integer)
    physicalDamageTaken           = Column(Integer)
    totalDamageDone               = Column(Integer)
    totalDamageDoneToChampions    = Column(Integer)
    totalDamageTaken              = Column(Integer)
    trueDamageDone                = Column(Integer)
    trueDamageDoneToChampions     = Column(Integer)
    trueDamageTaken               = Column(Integer)
    participant_frame = relationship('ParticipantFrameDto', back_populates='damage_stats', uselist=False)

class PositionDto(Base):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True, autoincrement=True)
    x  = Column(Integer)
    y  = Column(Integer)
    participant_frame = relationship('ParticipantFrameDto', back_populates='position', uselist=False)

class LeagueEntryDTO(Base):
    __tablename__ = 'league_entry'
    id             = Column(Integer, primary_key=True, autoincrement=True)
    mini_series_id = Column(Integer, ForeignKey('mini_series.id'), nullable=True)
    leagueId       = Column(String)
    puuid          = Column(String)
    queueType      = Column(String)
    tier           = Column(String)
    rank           = Column(String)
    leaguePoints   = Column(Integer)
    wins           = Column(Integer)
    losses         = Column(Integer)
    hotStreak      = Column(Boolean)
    veteran        = Column(Boolean)
    freshBlood     = Column(Boolean)
    inactive       = Column(Boolean)
    mini_series = relationship('MiniSeriesDTO', back_populates='league_entry', uselist=False)

class MiniSeriesDTO(Base):
    __tablename__ = 'mini_series'
    id       = Column(Integer, primary_key=True, autoincrement=True)
    losses   = Column(Integer)
    progress = Column(String)
    target   = Column(Integer)
    wins     = Column(Integer)
    league_entry = relationship('LeagueEntryDTO', back_populates='mini_series', uselist=False)


# ── Riot API Client ───────────────────────────────────────────────────────────

class RiotApiClient:
    """Handles all communication with the Riot API."""

    def __init__(self, api_key: str, base_url: str = "https://europe.api.riotgames.com", region_url: str = "https://euw1.api.riotgames.com"):
        self.headers    = {"X-Riot-Token": api_key}
        self.base_url   = base_url
        self.region_url = region_url

    def _get(self, url: str, params: dict = None) -> dict:
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_account(self, game_name: str, tag_line: str) -> dict:
        return self._get(f"{self.base_url}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}")

    def get_match_ids(self, puuid: str, count: int = 20) -> list:
        return self._get(f"{self.base_url}/lol/match/v5/matches/by-puuid/{puuid}/ids", params={"count": count})

    def get_match(self, match_id: str) -> dict:
        return self._get(f"{self.base_url}/lol/match/v5/matches/{match_id}")

    def get_match_timeline(self, match_id: str) -> dict:
        return self._get(f"{self.base_url}/lol/match/v5/matches/{match_id}/timeline")

    def get_league_entries(self, puuid: str) -> list:
        return self._get(f"{self.region_url}/lol/league/v4/entries/by-puuid/{puuid}")


# ── Database Manager ──────────────────────────────────────────────────────────

class DatabaseManager:
    """
    Handles all database operations.

    By default we keep existing data. Set AMADEUS_CLEAR_DB=true (or pass clear_on_init=True)
    to wipe tables on startup for a fresh run.
    """

    TABLES_TO_CLEAR = [
        'participant_frame', 'champion_stats', 'damage_stats', 'position',
        'participant_frames', 'events_timeline', 'frames_timeline',
        'participant_timeline', 'info_timeline', 'metadata_timeline', 'timeline',
        'match_ban', 'match_objective', 'match_objectives', 'match_team',
        'match_participant', 'match_info', 'match_metadata', 'match_id',
        'league_entry', 'mini_series', 'account'
    ]

    def __init__(self, db_url: str, clear_on_init: bool | None = None):
        if clear_on_init is None:
            flag = os.getenv("AMADEUS_CLEAR_DB", "false").lower()
            clear_on_init = flag in ("1", "true", "yes", "y")
        self.clear_on_init = clear_on_init

        self.engine  = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

        if self.clear_on_init:
            self._clear_all()

    def _clear_all(self):
        """Wipe all data so reruns start fresh."""
        # Drop and recreate all tables to ensure full cleanup (handles FK ordering).
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        print("[~] Database dropped and recreated — ready for fresh run.")

    def save_account(self, data: dict) -> AccountDto:
        with self.Session() as session:
            account = AccountDto(puuid=data['puuid'])
            session.add(account)
            session.commit()
            session.refresh(account)
            print(f"[+] Account saved: puuid={account.puuid[:8]}...")
            return account

    def save_match_ids(self, puuid: str, ids: list):
        with self.Session() as session:
            for match_id in ids:
                exists = session.query(MatchIdDto.id).filter_by(puuid=puuid, matchId=match_id).first()
                if exists:
                    continue
                session.add(MatchIdDto(puuid=puuid, matchId=match_id))
            session.commit()
        print(f"[+] Match IDs processed: {len(ids)} (new: {session.query(MatchIdDto).filter_by(puuid=puuid).count()})")

    def match_exists(self, match_id: str) -> bool:
        with self.Session() as session:
            return session.query(MatchMetadataDto.id).filter_by(matchId=match_id).first() is not None

    def timeline_exists(self, match_id: str) -> bool:
        with self.Session() as session:
            return session.query(MetadataTimeLineDto.id).filter_by(matchId=match_id).first() is not None

    def save_match(self, match_id: str, data: dict):
        meta_raw = data['metadata']
        info_raw = data['info']

        with self.Session() as session:
            # Skip if this match already exists
            if session.query(MatchMetadataDto.id).filter_by(matchId=match_id).first():
                print(f"[=] Match already stored: {match_id}")
                return

            meta = MatchMetadataDto(
                dataVersion=meta_raw['dataVersion'],
                matchId=meta_raw['matchId'],
                participants=meta_raw['participants']
            )
            session.add(meta)
            session.flush()

            info = MatchInfoDto(
                endOfGameResult=info_raw.get('endOfGameResult'),
                gameCreation=info_raw.get('gameCreation'),
                gameDuration=info_raw.get('gameDuration'),
                gameEndTimestamp=info_raw.get('gameEndTimestamp'),
                gameId=info_raw.get('gameId'),
                gameMode=info_raw.get('gameMode'),
                gameName=info_raw.get('gameName'),
                gameStartTimestamp=info_raw.get('gameStartTimestamp'),
                gameType=info_raw.get('gameType'),
                gameVersion=info_raw.get('gameVersion'),
                mapId=info_raw.get('mapId'),
                platformId=info_raw.get('platformId'),
                queueId=info_raw.get('queueId'),
                tournamentCode=info_raw.get('tournamentCode')
            )
            session.add(info)
            session.flush()

            for p in info_raw.get('participants', []):
                participant = ParticipantDto(**{
                    k: p.get(k) for k in ParticipantDto.__table__.columns.keys()
                    if k not in ('id', 'info_id')
                })
                participant.info_id = info.id
                session.add(participant)

            for t in info_raw.get('teams', []):
                obj_raw = t.get('objectives', {})

                def make_obj(key):
                    o = obj_raw.get(key, {})
                    obj = ObjectiveDto(first=o.get('first'), kills=o.get('kills'))
                    session.add(obj)
                    session.flush()
                    return obj.id

                objectives = ObjectivesDto(
                    baron_id=make_obj('baron'),
                    champion_id=make_obj('champion'),
                    dragon_id=make_obj('dragon'),
                    horde_id=make_obj('horde'),
                    inhibitor_id=make_obj('inhibitor'),
                    riftHerald_id=make_obj('riftHerald'),
                    tower_id=make_obj('tower')
                )
                session.add(objectives)
                session.flush()

                team = TeamDto(
                    info_id=info.id,
                    objectives_id=objectives.id,
                    teamId=t.get('teamId'),
                    win=t.get('win')
                )
                session.add(team)
                session.flush()

                for ban in t.get('bans', []):
                    session.add(BanDto(
                        team_id=team.id,
                        championId=ban.get('championId'),
                        pickTurn=ban.get('pickTurn')
                    ))

            session.commit()
        print(f"[+] Match saved: {match_id}")

    def save_timeline(self, match_id: str, data: dict):
        meta_raw = data['metadata']
        info_raw = data['info']

        with self.Session() as session:
            # Skip if timeline for this match already exists
            if session.query(MetadataTimeLineDto.id).filter_by(matchId=match_id).first():
                print(f"[=] Timeline already stored: {match_id}")
                return

            meta = MetadataTimeLineDto(
                dataVersion=meta_raw['dataVersion'],
                matchId=meta_raw['matchId'],
                participants=meta_raw['participants']
            )
            session.add(meta)
            session.flush()

            info = InfoTimeLineDto(
                endOfGameResult=info_raw.get('endOfGameResult'),
                frameInterval=info_raw.get('frameInterval'),
                gameId=info_raw.get('gameId')
            )
            session.add(info)
            session.flush()

            session.add(TimelineDto(meta_id=meta.id, info_id=info.id))

            for p in info_raw.get('participants', []):
                session.add(ParticipantTimeLineDto(
                    info_id=info.id,
                    participantId=p.get('participantId'),
                    puuid=p.get('puuid')
                ))

            for frame_raw in info_raw.get('frames', []):
                frame = FramesTimeLineDto(info_id=info.id, timestamp=frame_raw.get('timestamp'))
                session.add(frame)
                session.flush()

                for event in frame_raw.get('events', []):
                    session.add(EventsTimeLineDto(
                        frame_id=frame.id,
                        timestamp=event.get('timestamp'),
                        realTimestamp=event.get('realTimestamp'),
                        type=event.get('type')
                    ))

                pf_container = ParticipantFramesDto(frame_id=frame.id)
                session.add(pf_container)
                session.flush()

                for _, pf in frame_raw.get('participantFrames', {}).items():
                    cs = ChampionStatsDto(**{
                        k: pf.get('championStats', {}).get(k)
                        for k in ChampionStatsDto.__table__.columns.keys() if k != 'id'
                    })
                    session.add(cs)
                    session.flush()

                    ds = DamageStatsDto(**{
                        k: pf.get('damageStats', {}).get(k)
                        for k in DamageStatsDto.__table__.columns.keys() if k != 'id'
                    })
                    session.add(ds)
                    session.flush()

                    pos = PositionDto(
                        x=pf.get('position', {}).get('x'),
                        y=pf.get('position', {}).get('y')
                    )
                    session.add(pos)
                    session.flush()

                    session.add(ParticipantFrameDto(
                        participant_frames_id=pf_container.id,
                        champion_stats_id=cs.id,
                        damage_stats_id=ds.id,
                        position_id=pos.id,
                        currentGold=pf.get('currentGold'),
                        goldPerSecond=pf.get('goldPerSecond'),
                        jungleMinionsKilled=pf.get('jungleMinionsKilled'),
                        level=pf.get('level'),
                        minionsKilled=pf.get('minionsKilled'),
                        participantId=pf.get('participantId'),
                        timeEnemySpentControlled=pf.get('timeEnemySpentControlled'),
                        totalGold=pf.get('totalGold'),
                        xp=pf.get('xp')
                    ))

            session.commit()
        print(f"[+] Timeline saved: {match_id}")

    def save_league_entries(self, entries: list):
        with self.Session() as session:
            # Replace existing league entries with the latest snapshot.
            session.query(LeagueEntryDTO).delete()
            session.query(MiniSeriesDTO).delete()
            for e in entries:
                mini_series = None
                if 'miniSeries' in e:
                    ms = e['miniSeries']
                    mini_series = MiniSeriesDTO(
                        losses=ms.get('losses'),
                        progress=ms.get('progress'),
                        target=ms.get('target'),
                        wins=ms.get('wins')
                    )
                    session.add(mini_series)
                    session.flush()

                session.add(LeagueEntryDTO(
                    leagueId=e.get('leagueId'),
                    puuid=e.get('puuid'),
                    queueType=e.get('queueType'),
                    tier=e.get('tier'),
                    rank=e.get('rank'),
                    leaguePoints=e.get('leaguePoints'),
                    wins=e.get('wins'),
                    losses=e.get('losses'),
                    hotStreak=e.get('hotStreak'),
                    veteran=e.get('veteran'),
                    freshBlood=e.get('freshBlood'),
                    inactive=e.get('inactive'),
                    mini_series_id=mini_series.id if mini_series else None
                ))
            session.commit()
        print(f"[+] League entries saved.")


# ── Amadeus Pipeline ──────────────────────────────────────────────────────────

class AmadeusPipeline:
    """Orchestrates the full data ingestion flow."""

    def __init__(self, api_client: RiotApiClient, db_manager: DatabaseManager, rate_limit_sleep: float = 1.5):
        self.api = api_client
        self.db  = db_manager
        self.rate_limit_sleep = rate_limit_sleep

    def run(self, game_name: str, tag_line: str, match_count: int = 20):
        print(f"\n[Amadeus] Starting pipeline for {game_name}#{tag_line}\n")

        account_data = self.api.get_account(game_name, tag_line)
        account      = self.db.save_account(account_data)
        puuid        = account.puuid

        match_ids = self.api.get_match_ids(puuid, count=match_count)
        self.db.save_match_ids(puuid, match_ids)

        for i, match_id in enumerate(match_ids):
            print(f"[{i+1}/{len(match_ids)}] Processing {match_id}...")
            need_match    = not self.db.match_exists(match_id)
            need_timeline = not self.db.timeline_exists(match_id)

            if not need_match and not need_timeline:
                print(f"[=] Skipping {match_id} (already stored)")
                continue

            if need_match:
                self.db.save_match(match_id, self.api.get_match(match_id))
            if need_timeline:
                self.db.save_timeline(match_id, self.api.get_match_timeline(match_id))

            time.sleep(self.rate_limit_sleep)

        self.db.save_league_entries(self.api.get_league_entries(puuid))

        print("\n[Amadeus] ✓ Pipeline complete!")


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    DB_URL    = "sqlite:///C:/Users/offic/OneDrive/Dokumente/SpeiseUndGetraenkeKarten/_MittagsMenue/2024/Anlagen/Desktop/LeagueAnalyzerPython/db/LeagueToolDb.db"
    API_KEY   = os.getenv("RIOT_API_KEY")
    GAME_NAME = "Zai"
    TAG_LINE  = "Wins"
    CLEAR_DB  = os.getenv("AMADEUS_CLEAR_DB", "false").lower() in ("1", "true", "yes", "y")

    api = RiotApiClient(api_key=API_KEY)
    db  = DatabaseManager(db_url=DB_URL, clear_on_init=CLEAR_DB)

    pipeline = AmadeusPipeline(api_client=api, db_manager=db)
    pipeline.run(game_name=GAME_NAME, tag_line=TAG_LINE)

import time
from LeagueTool import HEADERS, DBSession
from LeagueTool import (
    get_account_by_riot_id,
    get_match_ids_by_puuid,
    get_match,
    get_match_timeline,
    get_league_entries_by_puuid
)
from LeagueToolTableCreation import (
    AccountDto, MatchIdDto, LeagueEntryDTO, MiniSeriesDTO,
    MatchDto, MatchMetadataDto, MatchInfoDto, ParticipantDto,
    TeamDto, BanDto,
    ObjectivesDto, ObjectiveDto,
    TimelineDto, MetadataTimeLineDto, InfoTimeLineDto,
    ParticipantTimeLineDto, FramesTimeLineDto, EventsTimeLineDto,
    ParticipantFramesDto, ParticipantFrameDto,
    ChampionStatsDto, DamageStatsDto, PositionDto
)

# ── 1. Account ────────────────────────────────────────────────────────────────

def save_account(game_name: str, tag_line: str) -> AccountDto:
    data = get_account_by_riot_id(game_name, tag_line)
    print(data)  # ← add here
    account = AccountDto(
        puuid    = data['puuid'],
        gameName = data.get('gameName'),
        tagLine  = data.get('tagLine')
    )
    DBSession.add(account)
    DBSession.commit()
    print(f"[+] Account saved: {game_name}#{tag_line}")
    return account


# ── 2. Match IDs ──────────────────────────────────────────────────────────────

def save_match_ids(puuid: str) -> list:
    ids = get_match_ids_by_puuid(puuid)
    for match_id in ids:
        row = MatchIdDto(puuid=puuid, matchId=match_id)
        DBSession.add(row)
    DBSession.commit()
    print(f"[+] {len(ids)} match IDs saved")
    return ids


# ── 3. Full Match ─────────────────────────────────────────────────────────────

def save_match(match_id: str):
    data     = get_match(match_id)
    meta_raw = data['metadata']
    info_raw = data['info']

    # metadata
    meta = MatchMetadataDto(
        dataVersion  = meta_raw['dataVersion'],
        matchId      = meta_raw['matchId'],
        participants = meta_raw['participants']
    )
    DBSession.add(meta)
    DBSession.flush()

    # info
    info = MatchInfoDto(
        meta_id            = meta.id,
        endOfGameResult    = info_raw.get('endOfGameResult'),
        gameCreation       = info_raw.get('gameCreation'),
        gameDuration       = info_raw.get('gameDuration'),
        gameEndTimestamp   = info_raw.get('gameEndTimestamp'),
        gameId             = info_raw.get('gameId'),
        gameMode           = info_raw.get('gameMode'),
        gameName           = info_raw.get('gameName'),
        gameStartTimestamp = info_raw.get('gameStartTimestamp'),
        gameType           = info_raw.get('gameType'),
        gameVersion        = info_raw.get('gameVersion'),
        mapId              = info_raw.get('mapId'),
        platformId         = info_raw.get('platformId'),
        queueId            = info_raw.get('queueId'),
        tournamentCode     = info_raw.get('tournamentCode')
    )
    DBSession.add(info)
    DBSession.flush()

    # participants
    for p in info_raw.get('participants', []):

    
        

        participant = ParticipantDto(**{
            k: p.get(k) for k in ParticipantDto.__table__.columns.keys()
            if k not in ('id', 'info_id',  'missions_id')
        })
        participant.info_id       = info.id
        DBSession.add(participant)

    # teams
    for t in info_raw.get('teams', []):
        obj_raw = t.get('objectives', {})

        def make_objective(key):
            o = obj_raw.get(key, {})
            obj = ObjectiveDto(first=o.get('first'), kills=o.get('kills'))
            DBSession.add(obj)
            DBSession.flush()
            return obj.id

        objectives = ObjectivesDto(
            baron_id      = make_objective('baron'),
            champion_id   = make_objective('champion'),
            dragon_id     = make_objective('dragon'),
            horde_id      = make_objective('horde'),
            inhibitor_id  = make_objective('inhibitor'),
            riftHerald_id = make_objective('riftHerald'),
            tower_id      = make_objective('tower')
        )
        DBSession.add(objectives)
        DBSession.flush()

        team = TeamDto(
            info_id       = info.id,
            objectives_id = objectives.id,
            teamId        = t.get('teamId'),
            win           = t.get('win')
        )
        DBSession.add(team)
        DBSession.flush()

        for ban_raw in t.get('bans', []):
            ban = BanDto(
                team_id    = team.id,
                championId = ban_raw.get('championId'),
                pickTurn   = ban_raw.get('pickTurn')
            )
            DBSession.add(ban)

    DBSession.commit()
    print(f"[+] Match saved: {match_id}")


# ── 4. Timeline ───────────────────────────────────────────────────────────────

def save_timeline(match_id: str):
    data     = get_match_timeline(match_id)
    meta_raw = data['metadata']
    info_raw = data['info']

    meta = MetadataTimeLineDto(
        dataVersion  = meta_raw['dataVersion'],
        matchId      = meta_raw['matchId'],
        participants = meta_raw['participants']
    )
    DBSession.add(meta)
    DBSession.flush()

    info = InfoTimeLineDto(
        endOfGameResult = info_raw.get('endOfGameResult'),
        frameInterval   = info_raw.get('frameInterval'),
        gameId          = info_raw.get('gameId')
    )
    DBSession.add(info)
    DBSession.flush()

    DBSession.add(TimelineDto(meta_id=meta.id, info_id=info.id))

    for p in info_raw.get('participants', []):
        DBSession.add(ParticipantTimeLineDto(
            info_id       = info.id,
            participantId = p.get('participantId'),
            puuid         = p.get('puuid')
        ))

    for frame_raw in info_raw.get('frames', []):
        frame = FramesTimeLineDto(
            info_id   = info.id,
            timestamp = frame_raw.get('timestamp')
        )
        DBSession.add(frame)
        DBSession.flush()

        for event_raw in frame_raw.get('events', []):
            DBSession.add(EventsTimeLineDto(
                frame_id      = frame.id,
                timestamp     = event_raw.get('timestamp'),
                realTimestamp = event_raw.get('realTimestamp'),
                type          = event_raw.get('type')
            ))

        pf_container = ParticipantFramesDto(frame_id=frame.id)
        DBSession.add(pf_container)
        DBSession.flush()

        for _, pf_raw in frame_raw.get('participantFrames', {}).items():
            cs_raw = pf_raw.get('championStats', {})
            champion_stats = ChampionStatsDto(**{
                k: cs_raw.get(k) for k in ChampionStatsDto.__table__.columns.keys()
                if k != 'id'
            })
            DBSession.add(champion_stats)
            DBSession.flush()

            ds_raw = pf_raw.get('damageStats', {})
            damage_stats = DamageStatsDto(**{
                k: ds_raw.get(k) for k in DamageStatsDto.__table__.columns.keys()
                if k != 'id'
            })
            DBSession.add(damage_stats)
            DBSession.flush()

            pos_raw = pf_raw.get('position', {})
            position = PositionDto(x=pos_raw.get('x'), y=pos_raw.get('y'))
            DBSession.add(position)
            DBSession.flush()

            DBSession.add(ParticipantFrameDto(
                participant_frames_id    = pf_container.id,
                champion_stats_id        = champion_stats.id,
                damage_stats_id          = damage_stats.id,
                position_id              = position.id,
                currentGold              = pf_raw.get('currentGold'),
                goldPerSecond            = pf_raw.get('goldPerSecond'),
                jungleMinionsKilled      = pf_raw.get('jungleMinionsKilled'),
                level                    = pf_raw.get('level'),
                minionsKilled            = pf_raw.get('minionsKilled'),
                participantId            = pf_raw.get('participantId'),
                timeEnemySpentControlled = pf_raw.get('timeEnemySpentControlled'),
                totalGold                = pf_raw.get('totalGold'),
                xp                       = pf_raw.get('xp')
            ))

    DBSession.commit()
    print(f"[+] Timeline saved: {match_id}")


# ── 5. League Entries ─────────────────────────────────────────────────────────

def save_league_entries(puuid: str):
    entries = get_league_entries_by_puuid(puuid)
    for e in entries:
        mini_series = None
        if 'miniSeries' in e:
            ms = e['miniSeries']
            mini_series = MiniSeriesDTO(
                losses   = ms.get('losses'),
                progress = ms.get('progress'),
                target   = ms.get('target'),
                wins     = ms.get('wins')
            )
            DBSession.add(mini_series)
            DBSession.flush()

        entry = LeagueEntryDTO(
            leagueId       = e.get('leagueId'),
            puuid          = e.get('puuid'),
            queueType      = e.get('queueType'),
            tier           = e.get('tier'),
            rank           = e.get('rank'),
            leaguePoints   = e.get('leaguePoints'),
            wins           = e.get('wins'),
            losses         = e.get('losses'),
            hotStreak      = e.get('hotStreak'),
            veteran        = e.get('veteran'),
            freshBlood     = e.get('freshBlood'),
            inactive       = e.get('inactive'),
            mini_series_id = mini_series.id if mini_series else None
        )
        DBSession.add(entry)

    DBSession.commit()
    print(f"[+] League entries saved for puuid: {puuid}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    GAME_NAME = "Zai"  # ← replace
    TAG_LINE  = "Wins"           # ← replace


    
    account   = save_account(GAME_NAME, TAG_LINE)
    puuid     = account.puuid
    match_ids = save_match_ids(puuid)

    for i, match_id in enumerate(match_ids):
        print(f"[{i+1}/{len(match_ids)}] Processing {match_id}...")
        save_match(match_id)
        save_timeline(match_id)
        time.sleep(1.5)

    save_league_entries(puuid)
    print("\n[✓] Full flow complete!")

   

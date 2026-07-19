# Content packs

Curriculum and campaign data live here (YAML/JSON). The app loads these files; do not hardcode quests in the frontend.

## Layout (target)

```
content/
  themes/
    detective_academy.yaml
  campaigns/
    detective_academy/
      campaign.yaml
      chapters/
        ch01/
          chapter.yaml
          quests/
            q01_two_sum.yaml
            ...
```

## Authoring

Follow `docs/CONTENT.md` and `docs/STORY_BIBLE.md`.  
Use `.cursor/skills/author-quest/SKILL.md` for canon; `.cursor/skills/write-quest-story/SKILL.md` for story slots.  
Validate story with `python scripts/validate_story.py <quest.yaml>`.

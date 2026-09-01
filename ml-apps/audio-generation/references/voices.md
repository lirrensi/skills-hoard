# Voice Catalog

Load this guide when choosing a voice for any audio generation task — TTS, podcasts, or long reads.

## Quick Picks

| Use case | Voice | Gender | Style |
|----------|-------|--------|-------|
| General purpose | `en-US-AriaNeural` | Female | Natural, warm, versatile |
| Authoritative / news | `en-US-GuyNeural` | Male | Clear, professional |
| Casual / friendly | `en-US-JennyNeural` | Female | Conversational, upbeat |
| British narration | `en-GB-SoniaNeural` | Female | Elegant, measured |
| Energetic promo | `en-US-TonyNeural` | Male | Dynamic, expressive |
| Deep / dramatic | `en-US-ChristopherNeural` | Male | Thoughtful, gravitas |
| Calm / meditation | `en-US-AnaNeural` | Female | Soft, gentle |
| Expert / analyst | `en-US-BrianNeural` | Male | Authoritative, steady |

## Listing Voices

```bash
# All available voices
edge-tts --list-voices

# Filter by language
edge-tts --list-voices | grep "en-"

# Filter by locale
edge-tts --list-voices | grep "en-US"

# Filter by gender
edge-tts --list-voices | grep "Male"
edge-tts --list-voices | grep "Female"
```

## English Voices

### en-US (American English)

| Voice | Gender | Best for |
|-------|--------|----------|
| `en-US-AriaNeural` | Female | General, narration, podcasts |
| `en-US-AnaNeural` | Female | Calm, gentle, children's content |
| `en-US-ChristopherNeural` | Male | Serious, documentary, deep |
| `en-US-EricNeural` | Male | Neutral, professional |
| `en-US-GuyNeural` | Male | News, authoritative, clear |
| `en-US-JennyNeural` | Female | Casual, friendly, conversational |
| `en-US-MichelleNeural` | Female | Warm, approachable |
| `en-US-RogerNeural` | Male | Energetic, broadcast |
| `en-US-SteffanNeural` | Male | Calm, measured |
| `en-US-TonyNeural` | Male | Dynamic, expressive, promos |

### en-GB (British English)

| Voice | Gender | Best for |
|-------|--------|----------|
| `en-GB-SoniaNeural` | Female | Elegant, literary, narration |
| `en-GB-RyanNeural` | Male | Clear, professional |
| `en-GB-LibbyNeural` | Female | Young, energetic |
| `en-GB-ThomasNeural` | Male | Warm, conversational |

### en-AU (Australian English)

| Voice | Gender | Best for |
|-------|--------|----------|
| `en-AU-NatashaNeural` | Female | Friendly, casual |
| `en-AU-WilliamNeural` | Male | Relaxed, clear |

### en-IN (Indian English)

| Voice | Gender | Best for |
|-------|--------|----------|
| `en-IN-NeerjaNeural` | Female | Warm, professional |
| `en-IN-PrabhatNeural` | Male | Clear, measured |

## Other Languages (Common)

### Spanish

| Voice | Locale | Gender |
|-------|--------|--------|
| `es-ES-ElviraNeural` | Spain | Female |
| `es-ES-AlvaroNeural` | Spain | Male |
| `es-MX-DaliaNeural` | Mexico | Female |
| `es-MX-JorgeNeural` | Mexico | Male |

### French

| Voice | Locale | Gender |
|-------|--------|--------|
| `fr-FR-DeniseNeural` | France | Female |
| `fr-FR-HenriNeural` | France | Male |

### German

| Voice | Locale | Gender |
|-------|--------|--------|
| `de-DE-KatjaNeural` | Germany | Female |
| `de-DE-ConradNeural` | Germany | Male |

### Portuguese

| Voice | Locale | Gender |
|-------|--------|--------|
| `pt-BR-FranciscaNeural` | Brazil | Female |
| `pt-BR-AntonioNeural` | Brazil | Male |
| `pt-PT-RaquelNeural` | Portugal | Female |

### Japanese

| Voice | Gender |
|-------|--------|
| `ja-JP-NanamiNeural` | Female |
| `ja-JP-KeitaNeural` | Male |

### Chinese (Mandarin)

| Voice | Locale | Gender |
|-------|--------|--------|
| `zh-CN-XiaoxiaoNeural` | China | Female |
| `zh-CN-YunxiNeural` | China | Male |
| `zh-TW-HsiaoChenNeural` | Taiwan | Female |

### Arabic

| Voice | Gender |
|-------|--------|
| `ar-SA-ZariyahNeural` | Female |
| `ar-SA-HamedNeural` | Male |

### Hindi

| Voice | Gender |
|-------|--------|
| `hi-IN-SwaraNeural` | Female |
| `hi-IN-MadhurNeural` | Male |

> For the full list of all 400+ voices, run `edge-tts --list-voices`.

## Voice Selection Guidelines

### By content type

| Content | Recommended voices | Why |
|---------|-------------------|-----|
| News / journalism | `en-US-GuyNeural`, `en-US-BrianNeural` | Authoritative, clear |
| Storytelling / fiction | `en-US-AriaNeural`, `en-GB-SoniaNeural` | Expressive, warm |
| Technical / academic | `en-US-ChristopherNeural`, `en-US-EricNeural` | Measured, precise |
| Marketing / promos | `en-US-TonyNeural`, `en-US-RogerNeural` | Energetic, dynamic |
| Meditation / wellness | `en-US-AnaNeural`, `en-US-SteffanNeural` | Calm, gentle |
| Children's content | `en-US-JennyNeural`, `en-US-AnaNeural` | Friendly, clear |
| Podcast host | `en-US-GuyNeural`, `en-US-AriaNeural` | Natural, versatile |
| Podcast guest | `en-US-ChristopherNeural`, `en-US-JennyNeural` | Distinct from host |

### By podcast pairing

Always pick voices that are **noticeably different**:

| Host | Guest | Contrast |
|------|-------|----------|
| `en-US-GuyNeural` (M) | `en-US-AriaNeural` (F) | Gender + style |
| `en-US-AriaNeural` (F) | `en-US-ChristopherNeural` (M) | Gender + depth |
| `en-US-JennyNeural` (F) | `en-US-TonyNeural` (M) | Gender + energy |
| `en-US-GuyNeural` (M) | `en-US-BrianNeural` (M) | Same gender, different tone |

### Matching language to content

**Always match the voice language to the text language.** A Spanish text read by an English voice will sound wrong — the pronunciation engine expects English phonemes.

If the content is multilingual, generate each language section with its matching voice, then concatenate.

## Testing a Voice

Before committing to a long generation, test with a short sample:

```bash
edge-tts --text "This is a test of the voice. The quick brown fox jumps over the lazy dog." \
  --voice en-US-AriaNeural --write-media test_voice.mp3
```

Listen for:
- Naturalness (does it sound human?)
- Clarity (every word understandable?)
- Tone match (does it fit the content?)
- Fatigue (could you listen to this for 30+ minutes?)

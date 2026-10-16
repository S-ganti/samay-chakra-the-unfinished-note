const places = [
      { title:'Enter the Ring', file:'01-enter-the-ring', time:'18:00 — 21:00', short:'18—21', raga:'Yaman', marker:'The threshold / Dusk', mood:'Arrival · Wonder · Amber silence', description:'An ancient circle opens in the overgrowth. The last light settles on stone, and the ordinary world begins to fall away.', alt:'Dusk environment concept with an overgrown giant stone ring, amber evening light, and layered vegetation.', color:'#d9a965', base:146.83, notes:[0,7,12,14,19], air:480, pace:5.7 },
      { title:'The Gathering', file:'02-the-gathering', time:'21:00 — 00:00', short:'21—00', raga:'Bihag', marker:'The courtyard / Nightfall', mood:'Belonging · Warmth · Shared light', description:'Crimson lanterns gather the night into a courtyard. Each small flame feels like a voice, held close beneath an immense sky.', alt:'Night courtyard environment concept with crimson lanterns, warm gathering spaces, and richly layered architecture.', color:'#db8c77', base:164.81, notes:[0,4,7,11,16], air:380, pace:4.6 },
      { title:'Eclipse', file:'03-eclipse', time:'00:00 — 03:00', short:'00—03', raga:'Malkauns', marker:'The mountain / Deep night', mood:'Vastness · Solitude · Electric hush', description:'A dark ring hangs above the mountain. Cold pines and wet rock catch a trace of magenta; everything else listens to the dark.', alt:'Midnight mountain environment concept with a giant eclipsed ring, cold blue pines, wet rocks, and magenta light.', color:'#a5a3d0', base:110, notes:[0,3,7,10,15], air:650, pace:7.2 },
      { title:'Brahma Muhurta', file:'04-brahma-muhurta', time:'03:00 — 06:00', short:'03—06', raga:'Lalit', marker:'The still lake / Before dawn', mood:'Stillness · Tenderness · First breath', description:'Mist drifts over a lake that has forgotten its edges. The stars leave delicate trails as the first pale breath of morning arrives.', alt:'Predawn lake environment concept with tender mist, star trails, layered reflections, and a quiet pale horizon.', color:'#a6c4bb', base:130.81, notes:[0,5,7,12,17], air:900, pace:6.4 },
      { title:'Diamond Ring', file:'05-diamond-ring', time:'06:00 — 09:00', short:'06—09', raga:'Bhairav', marker:'The cloud terraces / Sunrise', mood:'Release · Radiance · A beginning', description:'White gold spills through the ring. Terraces rise out of cloud, and for a moment the whole world seems light enough to fly.', alt:'Sunrise environment concept with a white-gold sun ring rising above cloud terraces and luminous layered architecture.', color:'#e5ce8b', base:174.61, notes:[0,7,12,16,19], air:1300, pace:4.9 },
      { title:'Dispersal', file:'06-dispersal', time:'09:00 — 12:00', short:'09—12', raga:'Todi', marker:'The city / Late morning', mood:'Everyday grace · Motion · Returning', description:'Banyan shade falls across cream streets. An auto-rickshaw passes; coffee steams. The extraordinary returns gently to everyday life.', alt:'Late-morning Bengaluru environment concept with banyan trees, cream streets, an auto-rickshaw, and a coffee stall.', color:'#bec78e', base:146.83, notes:[0,5,9,12,14], air:1100, pace:4.1 },
      { title:'Zero Shadow', file:'07-zero-shadow', time:'12:00 — 15:00', short:'12—15', raga:'Bhimpalasi', marker:'The observatory / High noon', mood:'Clarity · Suspension · Almost silence', description:'At the centre of the astronomical court, light becomes architecture. Bleached ivory, precise circles, and the smallest possible shadow.', alt:'High-noon astronomical courtyard environment concept with bleached ivory structures, circular instruments, and nearly absent shadows.', color:'#d6d0b7', base:196, notes:[0,7,12,14,19], air:1800, pace:8 },
      { title:'Return', file:'08-return', time:'15:00 — 18:00', short:'15—18', raga:'Marwa', marker:'The forest road / Afternoon', mood:'Remembrance · Renewal · Coming home', description:'Honey light follows the forest road. The broken circle has come together again; the way back is familiar, and quietly changed.', alt:'Afternoon forest-road environment concept with honey-colored light and a broken stone ring rebuilt among layered trees.', color:'#d5ae74', base:130.81, notes:[0,4,7,12,16], air:700, pace:6.1 }
    ];
    class Ambience {
      constructor() {
        const Context = window.AudioContext || window.webkitAudioContext;
        if (!Context) throw new Error('Web Audio unavailable');
        this.context = new Context();
        this.master = this.context.createGain();
        this.master.gain.value = 0;
        this.master.connect(this.context.destination);
        this.voices = new Set();
        this.timer = null;
        this.volume = .25;
        this.enabled = false;
      }
      setVolume(value) {
        this.volume = value;
        this.master.gain.setTargetAtTime(this.enabled ? .24 * value : 0, this.context.currentTime, .2);
      }
      async start(place) {
        await this.context.resume();
        this.enabled = true;
        this.setVolume(this.volume);
        this.changePlace(place);
      }
      stop() {
        this.enabled = false;
        this.master.gain.setTargetAtTime(0, this.context.currentTime, .3);
        this.clearVoices();
      }
      clearVoices() {
        clearInterval(this.timer);
        const now = this.context.currentTime;
        for (const voice of this.voices) {
          voice.gain.gain.cancelScheduledValues(now);
          voice.gain.gain.setTargetAtTime(0, now, .3);
          try { voice.source.stop(now + 1.5); } catch {}
        }
        this.voices.clear();
      }
      connectVoice(source, gain, filter) {
        if (filter) { source.connect(filter); filter.connect(gain); }
        else source.connect(gain);
        gain.connect(this.master);
        const voice = { source, gain };
        this.voices.add(voice);
        source.onended = () => { source.disconnect(); gain.disconnect(); if(filter) filter.disconnect(); this.voices.delete(voice); };
        return voice;
      }
      tone(frequency, duration, strength) {
        const now = this.context.currentTime;
        const oscillator = this.context.createOscillator();
        const gain = this.context.createGain();
        oscillator.type = 'sine';
        oscillator.frequency.value = frequency;
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(strength, now + Math.min(2, duration * .3));
        gain.gain.exponentialRampToValueAtTime(.0001, now + duration);
        this.connectVoice(oscillator, gain);
        oscillator.start(now);
        oscillator.stop(now + duration + .1);
      }
      changePlace(place) {
        this.clearVoices();
        if (!this.enabled) return;
        const now = this.context.currentTime;
        for (const ratio of [.5, 1, 1.5]) {
          const oscillator = this.context.createOscillator();
          const gain = this.context.createGain();
          oscillator.frequency.value = place.base * ratio;
          oscillator.detune.value = ratio === 1.5 ? 3 : 0;
          gain.gain.setValueAtTime(0, now);
          gain.gain.linearRampToValueAtTime(ratio === .5 ? .12 : .07, now + 3);
          this.connectVoice(oscillator, gain);
          oscillator.start(now);
        }
        const buffer = this.context.createBuffer(1, this.context.sampleRate * 5, this.context.sampleRate);
        const data = buffer.getChannelData(0);
        let brown = 0;
        for (let i = 0; i < data.length; i++) { brown = (brown + (Math.random() * 2 - 1) * .02) / 1.02; data[i] = brown * 3.5; }
        const wind = this.context.createBufferSource();
        wind.buffer = buffer;
        wind.loop = true;
        const filter = this.context.createBiquadFilter();
        filter.type = 'lowpass'; filter.frequency.value = place.air; filter.Q.value = .4;
        const windGain = this.context.createGain();
        windGain.gain.setValueAtTime(0, now); windGain.gain.linearRampToValueAtTime(.13, now + 4);
        this.connectVoice(wind, windGain, filter); wind.start(now);
        let step = 0;
        const melody = [0,2,1,4,3,2,4,1];
        const phrase = () => {
          const note = place.notes[melody[step++ % melody.length] % place.notes.length];
          this.tone(place.base * Math.pow(2, note / 12), place.pace * 1.7, .14);
          this.tone(place.base * Math.pow(2, note / 12) * 2.001, place.pace * 1.1, .025);
        };
        phrase();
        this.timer = setInterval(phrase, place.pace * 1000);
      }
    }

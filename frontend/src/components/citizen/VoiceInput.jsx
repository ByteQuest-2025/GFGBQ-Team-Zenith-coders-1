import { useState, useEffect } from 'react';
import { Button } from '../ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Mic, MicOff, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';

export default function VoiceInput({ onTranscript, onLanguageDetected }) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [interimTranscript, setInterimTranscript] = useState('');
  const [recognition, setRecognition] = useState(null);
  const [isSupported, setIsSupported] = useState(true);

  useEffect(() => {
    // Check if browser supports Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      setIsSupported(false);
      return;
    }

    const recognitionInstance = new SpeechRecognition();
    recognitionInstance.continuous = true;
    recognitionInstance.interimResults = true;
    recognitionInstance.lang = 'en-US'; // Default to English

    recognitionInstance.onstart = () => {
      setIsListening(true);
      toast.success('Listening... Speak now');
    };

    recognitionInstance.onend = () => {
      setIsListening(false);
    };

    recognitionInstance.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
      
      if (event.error === 'no-speech') {
        toast.error('No speech detected. Please try again.');
      } else if (event.error === 'not-allowed') {
        toast.error('Microphone access denied. Please enable it in browser settings.');
      } else {
        toast.error('Speech recognition error. Please try again.');
      }
    };

    recognitionInstance.onresult = (event) => {
      let interim = '';
      let final = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcriptPart = event.results[i][0].transcript;
        
        if (event.results[i].isFinal) {
          final += transcriptPart + ' ';
        } else {
          interim += transcriptPart;
        }
      }

      setInterimTranscript(interim);
      
      if (final) {
        const newTranscript = transcript + final;
        setTranscript(newTranscript);
        setInterimTranscript('');
        
        // Detect language from transcript
        const detectedLang = detectLanguage(newTranscript);
        if (detectedLang && onLanguageDetected) {
          onLanguageDetected(detectedLang);
        }
        
        // Pass transcript to parent
        if (onTranscript) {
          onTranscript(newTranscript.trim());
        }
      }
    };

    setRecognition(recognitionInstance);

    return () => {
      if (recognitionInstance) {
        recognitionInstance.stop();
      }
    };
  }, [transcript, onTranscript, onLanguageDetected]);

  const detectLanguage = (text) => {
    // Simple language detection based on character patterns
    const hindiPattern = /[\u0900-\u097F]/;
    const tamilPattern = /[\u0B80-\u0BFF]/;
    
    if (hindiPattern.test(text)) {
      return 'hi';
    } else if (tamilPattern.test(text)) {
      return 'ta';
    }
    return 'en';
  };

  const startListening = () => {
    if (!recognition) return;
    
    try {
      recognition.start();
    } catch (error) {
      console.error('Error starting recognition:', error);
      toast.error('Could not start voice input');
    }
  };

  const stopListening = () => {
    if (!recognition) return;
    
    try {
      recognition.stop();
      toast.success('Voice input stopped');
    } catch (error) {
      console.error('Error stopping recognition:', error);
    }
  };

  const clearTranscript = () => {
    setTranscript('');
    setInterimTranscript('');
    if (onTranscript) {
      onTranscript('');
    }
  };

  const changeLanguage = (lang) => {
    if (!recognition) return;
    
    const wasListening = isListening;
    if (wasListening) {
      recognition.stop();
    }
    
    const langCodes = {
      en: 'en-US',
      hi: 'hi-IN',
      ta: 'ta-IN'
    };
    
    recognition.lang = langCodes[lang] || 'en-US';
    toast.success(`Language changed to ${lang.toUpperCase()}`);
    
    if (wasListening) {
      setTimeout(() => recognition.start(), 500);
    }
  };

  if (!isSupported) {
    return (
      <Card>
        <CardContent className="p-6 text-center">
          <p className="text-red-500">Voice input is not supported in your browser.</p>
          <p className="text-sm text-gray-500 mt-2">
            Please use Chrome, Edge, or Safari for voice input.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Mic className="w-5 h-5" />
          Voice Input
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Language Selection */}
        <div className="flex gap-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => changeLanguage('en')}
          >
            English
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => changeLanguage('hi')}
          >
            Hindi
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => changeLanguage('ta')}
          >
            Tamil
          </Button>
        </div>

        {/* Voice Control Buttons */}
        <div className="flex gap-2">
          {!isListening ? (
            <Button
              onClick={startListening}
              className="flex-1"
              variant="default"
            >
              <Mic className="mr-2 h-4 w-4" />
              Start Recording
            </Button>
          ) : (
            <Button
              onClick={stopListening}
              className="flex-1"
              variant="destructive"
            >
              <MicOff className="mr-2 h-4 w-4" />
              Stop Recording
            </Button>
          )}
          
          {transcript && (
            <Button
              onClick={clearTranscript}
              variant="outline"
            >
              Clear
            </Button>
          )}
        </div>

        {/* Transcript Display */}
        {(transcript || interimTranscript || isListening) && (
          <div className="min-h-[100px] p-4 bg-gray-50 rounded-lg border">
            {isListening && (
              <div className="flex items-center gap-2 mb-2">
                <Loader2 className="h-4 w-4 animate-spin text-red-500" />
                <span className="text-sm text-red-500 font-medium">Listening...</span>
              </div>
            )}
            
            <p className="text-gray-900 whitespace-pre-wrap">
              {transcript}
              {interimTranscript && (
                <span className="text-gray-400">{interimTranscript}</span>
              )}
            </p>
            
            {!transcript && !interimTranscript && isListening && (
              <p className="text-gray-400 italic">Speak now...</p>
            )}
          </div>
        )}

        {/* Word Count */}
        {transcript && (
          <div className="text-sm text-gray-500">
            Words: {transcript.trim().split(/\s+/).filter(Boolean).length}
          </div>
        )}

        {/* Instructions */}
        <div className="text-xs text-gray-500 space-y-1">
          <p>Tips for better recognition:</p>
          <ul className="list-disc list-inside space-y-1">
            <li>Speak clearly and at a moderate pace</li>
            <li>Minimize background noise</li>
            <li>Select the language before recording</li>
            <li>Click Stop when finished speaking</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}

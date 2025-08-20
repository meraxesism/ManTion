import React, { useState, useEffect } from 'react';
import { Play, Settings, Camera, Monitor, Cpu, Wifi, AlertTriangle, CheckCircle, X, Save } from 'lucide-react';

const API_URL = 'http://localhost:5000/api';

const ManTionApp: React.FC = () => {
  const [isSystemActive, setIsSystemActive] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [systemStatus, setSystemStatus] = useState<'idle' | 'starting' | 'running' | 'stopping'>('idle');
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'connecting'>('disconnected');
  const [statusPollingInterval, setStatusPollingInterval] = useState<NodeJS.Timeout | null>(null);
  
  // Settings state
  const [settings, setSettings] = useState({
    cameraIndex: 0,
    detectionThreshold: 0.4,
    maxHands: 2,
    alarmEnabled: true,
    debounceMs: 400,
    resolution: '1280x720',
    fps: 30
  });

  const [availableCameras, setAvailableCameras] = useState<{index: number, name: string, status: string}[]>([]);

  // Fetch initial settings and status from backend
  useEffect(() => {
    fetch(`${API_URL}/settings`)
      .then(res => res.json())
      .then(data => setSettings(data));
    fetch(`${API_URL}/status`)
      .then(res => res.json())
      .then(data => {
        setIsSystemActive(data.isSystemActive);
        setSystemStatus(data.systemStatus);
        setConnectionStatus(data.connectionStatus);
      });
  }, []);

  // Fetch cameras when settings panel is opened
  useEffect(() => {
    if (showSettings) {
      fetch(`${API_URL}/cameras`)
        .then(res => res.json())
        .then(data => setAvailableCameras(data));
    }
  }, [showSettings]);

  const handleStartSystem = async () => {
    setSystemStatus('starting');
    setConnectionStatus('connecting');
    try {
      const res = await fetch(`${API_URL}/start`, { 
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings)
      });
      
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      
      const data = await res.json();
      
      if (data.success) {
        setIsSystemActive(data.status.isSystemActive);
        setSystemStatus(data.status.systemStatus);
        setConnectionStatus(data.status.connectionStatus);
        
        // Start polling for camera status updates
        startStatusPolling();
      } else {
        throw new Error(data.error || 'Failed to start system');
      }
    } catch (e) {
      console.error('Failed to start system:', e);
      setSystemStatus('idle');
      setConnectionStatus('disconnected');
      alert(`Failed to start system: ${e instanceof Error ? e.message : 'Unknown error'}`);
    }
  };

  const handleStopSystem = async () => {
    setSystemStatus('stopping');
    try {
      const res = await fetch(`${API_URL}/stop`, { method: 'POST' });
      const data = await res.json();
      setIsSystemActive(data.status.isSystemActive);
      setSystemStatus(data.status.systemStatus);
      setConnectionStatus(data.status.connectionStatus);
      
      // Stop status polling
      stopStatusPolling();
    } catch (e) {
      console.error('Failed to stop system:', e);
      setSystemStatus('idle');
      setConnectionStatus('disconnected');
    }
  };

  const handleSettingsChange = (key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const saveSettings = async () => {
    try {
      await fetch(`${API_URL}/settings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
      });
    } catch (e) {}
    setShowSettings(false);
  };

  // Status polling functions
  const startStatusPolling = () => {
    if (statusPollingInterval) return; // Already polling
    
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_URL}/camera-status`);
        const cameraStatus = await res.json();
        
        // Update UI based on camera status
        if (cameraStatus.active) {
          setSystemStatus('running');
          setConnectionStatus('connected');
        }
      } catch (e) {
        console.error('Status polling error:', e);
      }
    }, 1000); // Poll every second
    
    setStatusPollingInterval(interval);
  };

  const stopStatusPolling = () => {
    if (statusPollingInterval) {
      clearInterval(statusPollingInterval);
      setStatusPollingInterval(null);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopStatusPolling();
    };
  }, [statusPollingInterval]);

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden relative">
      {/* Animated Cyberpunk Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-blue-900/20 to-cyan-900/20">
        {/* Moving Grid Lines */}
        <div className="absolute inset-0 bg-moving-grid opacity-30"></div>
        
        {/* Floating Geometric Shapes */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden">
          {[...Array(20)].map((_, i) => (
            <div
              key={`hex-${i}`}
              className="absolute border border-cyan-400/30 animate-float"
              style={{
                left: `${Math.random() * 120 - 10}%`,
                top: `${Math.random() * 120 - 10}%`,
                width: `${Math.random() * 40 + 20}px`,
                height: `${Math.random() * 40 + 20}px`,
                clipPath: 'polygon(30% 0%, 70% 0%, 100% 50%, 70% 100%, 30% 100%, 0% 50%)',
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${Math.random() * 10 + 15}s`
              }}
            />
          ))}
        </div>

        {/* Circuit-like Lines */}
        <div className="absolute inset-0">
          {[...Array(8)].map((_, i) => (
            <div
              key={`circuit-${i}`}
              className="absolute bg-gradient-to-r from-transparent via-cyan-400/20 to-transparent animate-circuit-flow"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                width: '200px',
                height: '2px',
                transform: `rotate(${Math.random() * 360}deg)`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${Math.random() * 4 + 6}s`
              }}
            />
          ))}
        </div>

        {/* Data Stream Effects */}
        <div className="absolute inset-0">
          {[...Array(5)].map((_, i) => (
            <div
              key={`stream-${i}`}
              className="absolute flex flex-col space-y-2 animate-data-stream opacity-60"
              style={{
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 4}s`,
                animationDuration: `${Math.random() * 8 + 12}s`
              }}
            >
              {[...Array(20)].map((_, j) => (
                <div
                  key={j}
                  className="w-1 bg-green-400 rounded-full"
                  style={{
                    height: `${Math.random() * 20 + 5}px`,
                    opacity: Math.random() * 0.8 + 0.2
                  }}
                />
              ))}
            </div>
          ))}
        </div>

        {/* Pulsating Particles */}
        <div className="absolute top-0 left-0 w-full h-full">
          {[...Array(100)].map((_, i) => (
            <div
              key={`particle-${i}`}
              className="absolute animate-particle-float"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${Math.random() * 6 + 8}s`
              }}
            >
              <div 
                className="bg-cyan-400 rounded-full animate-particle-glow"
                style={{
                  width: `${Math.random() * 6 + 2}px`,
                  height: `${Math.random() * 6 + 2}px`,
                  animationDelay: `${Math.random() * 2}s`,
                  animationDuration: `${Math.random() * 3 + 2}s`
                }}
              />
            </div>
          ))}
        </div>

        {/* Scanning Lines */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute w-full h-0.5 bg-gradient-to-r from-transparent via-cyan-400/80 to-transparent animate-scan-vertical"></div>
          <div className="absolute h-full w-0.5 bg-gradient-to-b from-transparent via-purple-400/60 to-transparent animate-scan-horizontal"></div>
        </div>

        {/* Matrix-style Digital Rain */}
        <div className="absolute inset-0 overflow-hidden opacity-20">
          {[...Array(15)].map((_, i) => (
            <div
              key={`matrix-${i}`}
              className="absolute top-0 text-green-400 text-xs font-mono animate-matrix-rain leading-none"
              style={{
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${Math.random() * 5 + 10}s`
              }}
            >
              {Array.from({ length: 30 }, () => 
                Math.random() > 0.5 ? String.fromCharCode(0x30A0 + Math.random() * 96) : Math.floor(Math.random() * 2)
              ).join('')}
            </div>
          ))}
        </div>
      </div>

      {/* Header */}
      <header className="relative z-10 p-6 border-b border-cyan-500/30">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center">
              <Monitor className="w-6 h-6 text-black" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                ManTion
              </h1>
              <p className="text-sm text-gray-400">Gesture-Controlled Safety System</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${
                connectionStatus === 'connected' ? 'bg-green-400' : 
                connectionStatus === 'connecting' ? 'bg-yellow-400 animate-pulse' : 
                'bg-red-400'
              }`}></div>
              <span className="text-sm text-gray-400">
                {connectionStatus === 'connected' ? 'System Online' : 
                 connectionStatus === 'connecting' ? 'Connecting...' : 
                 'System Offline'}
              </span>
            </div>
            
            <div className="flex items-center space-x-2 px-3 py-1 bg-gray-800/50 rounded-lg border border-gray-700">
              <Cpu className="w-4 h-4 text-cyan-400" />
              <span className="text-sm">YOLOv8 + MediaPipe</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 flex items-center justify-center min-h-[calc(100vh-120px)] p-6">
        <div className="max-w-4xl w-full">
          {!showSettings ? (
            <>
              {/* System Status */}
              <div className="text-center mb-12">
                <div className={`inline-flex items-center space-x-3 px-6 py-3 rounded-full border-2 ${
                  systemStatus === 'running' ? 'border-green-400 bg-green-400/10' :
                  systemStatus === 'starting' || systemStatus === 'stopping' ? 'border-yellow-400 bg-yellow-400/10' :
                  'border-gray-600 bg-gray-600/10'
                }`}>
                  {systemStatus === 'running' && <CheckCircle className="w-6 h-6 text-green-400" />}
                  {(systemStatus === 'starting' || systemStatus === 'stopping') && <div className="w-6 h-6 border-2 border-yellow-400 border-t-transparent rounded-full animate-spin"></div>}
                  {systemStatus === 'idle' && <AlertTriangle className="w-6 h-6 text-gray-400" />}
                  
                  <span className="text-lg font-semibold">
                    {systemStatus === 'running' ? 'Detection System Active' :
                     systemStatus === 'starting' ? 'Initializing System...' :
                     systemStatus === 'stopping' ? 'Shutting Down...' :
                     'System Standby'}
                  </span>
                </div>
              </div>

              {/* Control Buttons */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-2xl mx-auto">
                {/* Start/Stop Button */}
                <button
                  onClick={isSystemActive ? handleStopSystem : handleStartSystem}
                  disabled={systemStatus === 'starting' || systemStatus === 'stopping'}
                  className={`group relative overflow-hidden p-8 rounded-2xl border-2 transition-all duration-300 animate-hologram ${
                    isSystemActive 
                      ? 'border-red-500 bg-red-500/10 hover:bg-red-500/20' 
                      : 'border-cyan-500 bg-cyan-500/10 hover:bg-cyan-500/20'
                  } ${systemStatus === 'starting' || systemStatus === 'stopping' ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105 glow-effect'}`}
                >
                  {/* Animated border overlay */}
                  <div className="absolute inset-0 border-2 border-transparent bg-gradient-to-r from-cyan-400/0 via-cyan-400/30 to-cyan-400/0 animate-pulse rounded-2xl"></div>
                  
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
                  
                  <div className="relative flex flex-col items-center space-y-4">
                    <div className={`w-16 h-16 rounded-full flex items-center justify-center relative ${
                      isSystemActive ? 'bg-red-500/20' : 'bg-cyan-500/20'
                    }`}>
                      {/* Pulsing ring effect */}
                      <div className={`absolute inset-0 rounded-full animate-ping ${
                        isSystemActive ? 'bg-red-400/30' : 'bg-cyan-400/30'
                      }`}></div>
                      
                      {systemStatus === 'starting' || systemStatus === 'stopping' ? (
                        <div className="w-8 h-8 border-2 border-white border-t-transparent rounded-full animate-spin z-10"></div>
                      ) : (
                        <Play className={`w-8 h-8 z-10 ${isSystemActive ? 'text-red-400 rotate-45' : 'text-cyan-400'}`} />
                      )}
                    </div>
                    <div className="text-center">
                      <h3 className="text-xl font-bold">
                        {isSystemActive ? 'Stop Detection' : 'Start Detection'}
                      </h3>
                      <p className="text-sm text-gray-400 mt-1">
                        {isSystemActive ? 'Deactivate gesture control' : 'Begin monitoring for gestures'}
                      </p>
                    </div>
                  </div>
                </button>

                {/* Settings Button */}
                <button
                  onClick={() => setShowSettings(true)}
                  className="group relative overflow-hidden p-8 rounded-2xl border-2 border-purple-500 bg-purple-500/10 hover:bg-purple-500/20 transition-all duration-300 hover:scale-105 animate-hologram glow-effect"
                >
                  {/* Animated circuit pattern overlay */}
                  <div className="absolute inset-0 opacity-20">
                    <div className="absolute top-4 left-4 w-8 h-8 border border-purple-400/50">
                      <div className="absolute top-1 left-1 w-2 h-2 bg-purple-400 animate-pulse"></div>
                    </div>
                    <div className="absolute bottom-4 right-4 w-6 h-6 border border-purple-400/50 rotate-45">
                      <div className="absolute top-1 left-1 w-1 h-1 bg-purple-400 animate-pulse"></div>
                    </div>
                    <div className="absolute top-1/2 left-8 w-16 h-0.5 bg-gradient-to-r from-purple-400/50 to-transparent"></div>
                  </div>
                  
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
                  
                  <div className="relative flex flex-col items-center space-y-4">
                    <div className="w-16 h-16 rounded-full bg-purple-500/20 flex items-center justify-center relative">
                      {/* Rotating outer ring */}
                      <div className="absolute inset-0 border-2 border-purple-400/30 rounded-full animate-spin"></div>
                      <div className="absolute inset-2 border border-purple-400/20 rounded-full animate-pulse"></div>
                      
                      <Settings className="w-8 h-8 text-purple-400 group-hover:rotate-180 transition-transform duration-500 z-10" />
                    </div>
                    <div className="text-center">
                      <h3 className="text-xl font-bold">System Settings</h3>
                      <p className="text-sm text-gray-400 mt-1">Configure cameras and detection</p>
                    </div>
                  </div>
                </button>
              </div>

              {/* Status Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 max-w-4xl mx-auto">
                <div className="p-6 rounded-xl bg-gray-800/30 border border-gray-700/50 backdrop-blur-sm relative overflow-hidden group hover:border-cyan-400/50 transition-all duration-300">
                  {/* Animated data flow */}
                  <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-400/60 to-transparent animate-pulse"></div>
                  <div className="absolute bottom-0 right-0 w-1 h-full bg-gradient-to-b from-transparent via-cyan-400/40 to-transparent"></div>
                  
                  <div className="flex items-center justify-between mb-4 relative z-10">
                    <div className="relative">
                      <Camera className="w-6 h-6 text-cyan-400" />
                      <div className="absolute -top-1 -right-1 w-3 h-3 bg-cyan-400 rounded-full animate-ping opacity-30"></div>
                    </div>
                    <span className="text-sm text-green-400 px-2 py-1 rounded bg-green-400/20 animate-pulse">Active</span>
                  </div>
                  <h4 className="font-semibold mb-2">Camera {settings.cameraIndex}</h4>
                  <p className="text-sm text-gray-400">{settings.resolution} @ {settings.fps}fps</p>
                  
                  {/* Signal strength indicator */}
                  <div className="flex items-center mt-3 space-x-1">
                    {[...Array(4)].map((_, i) => (
                      <div
                        key={i}
                        className={`w-1 bg-cyan-400 rounded-full animate-pulse`}
                        style={{
                          height: `${(i + 1) * 4}px`,
                          animationDelay: `${i * 0.2}s`
                        }}
                      />
                    ))}
                  </div>
                </div>

                <div className="p-6 rounded-xl bg-gray-800/30 border border-gray-700/50 backdrop-blur-sm relative overflow-hidden group hover:border-purple-400/50 transition-all duration-300">
                  {/* Processing animation */}
                  <div className="absolute top-0 left-0 w-full h-full opacity-10">
                    <div className="absolute top-3 left-3 w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                    <div className="absolute top-6 right-8 w-1 h-1 bg-purple-400 rounded-full animate-ping"></div>
                    <div className="absolute bottom-4 left-6 w-1.5 h-1.5 bg-purple-400 rounded-full animate-pulse"></div>
                  </div>
                  
                  <div className="flex items-center justify-between mb-4 relative z-10">
                    <div className="relative">
                      <Wifi className="w-6 h-6 text-purple-400" />
                      <div className="absolute inset-0 animate-pulse">
                        <div className="absolute top-1 left-1 w-1 h-1 bg-purple-400 rounded-full animate-ping"></div>
                      </div>
                    </div>
                    <span className="text-sm text-blue-400 px-2 py-1 rounded bg-blue-400/20">Ready</span>
                  </div>
                  <h4 className="font-semibold mb-2">Detection Engine</h4>
                  <p className="text-sm text-gray-400">Threshold: {settings.detectionThreshold}</p>
                  
                  {/* Processing indicator */}
                  <div className="mt-3 h-1 bg-gray-600 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-purple-400 to-blue-400 rounded-full animate-pulse" style={{ width: '85%' }}></div>
                  </div>
                </div>

                <div className="p-6 rounded-xl bg-gray-800/30 border border-gray-700/50 backdrop-blur-sm relative overflow-hidden group hover:border-yellow-400/50 transition-all duration-300">
                  {/* Alert pulse animation */}
                  <div className="absolute inset-0 opacity-5">
                    <div className="absolute inset-0 bg-yellow-400 animate-pulse rounded-xl"></div>
                  </div>
                  
                  <div className="flex items-center justify-between mb-4 relative z-10">
                    <div className="relative">
                      <AlertTriangle className="w-6 h-6 text-yellow-400" />
                      {settings.alarmEnabled && (
                        <div className="absolute -inset-1 border border-yellow-400/30 rounded-full animate-ping"></div>
                      )}
                    </div>
                    <span className={`text-sm px-2 py-1 rounded ${settings.alarmEnabled ? 'text-green-400 bg-green-400/20 animate-pulse' : 'text-red-400 bg-red-400/20'}`}>
                      {settings.alarmEnabled ? 'Enabled' : 'Disabled'}
                    </span>
                  </div>
                  <h4 className="font-semibold mb-2">Safety Alarms</h4>
                  <p className="text-sm text-gray-400">Emergency response system</p>
                  
                  {/* Status indicator */}
                  <div className="flex items-center mt-3 space-x-2">
                    <div className={`w-2 h-2 rounded-full ${settings.alarmEnabled ? 'bg-green-400 animate-ping' : 'bg-red-400'}`}></div>
                    <div className="text-xs text-gray-500">
                      {settings.alarmEnabled ? 'Monitoring' : 'Standby'}
                    </div>
                  </div>
                </div>
              </div>
            </>
          ) : (
            /* Settings Panel */
            <div className="max-w-2xl mx-auto">
              <div className="bg-gray-800/40 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-8">
                <div className="flex items-center justify-between mb-8">
                  <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
                    System Settings
                  </h2>
                  <button
                    onClick={() => setShowSettings(false)}
                    className="p-2 rounded-lg bg-gray-700/50 hover:bg-gray-700 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <div className="space-y-6">
                  {/* Camera Selection */}
                  <div>
                    <label className="block text-sm font-semibold text-gray-300 mb-3">
                      Camera Source
                    </label>
                    <div className="space-y-2">
                      {availableCameras.map((camera) => (
                        <div
                          key={camera.index}
                          onClick={() => camera.status !== 'unavailable' && handleSettingsChange('cameraIndex', camera.index)}
                          className={`p-4 rounded-lg border cursor-pointer transition-all ${
                            settings.cameraIndex === camera.index
                              ? 'border-cyan-400 bg-cyan-400/10'
                              : camera.status === 'unavailable'
                              ? 'border-gray-600 bg-gray-700/20 opacity-50 cursor-not-allowed'
                              : 'border-gray-600 bg-gray-700/20 hover:border-gray-500'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <Camera className="w-5 h-5 text-gray-400" />
                              <div>
                                <div className="font-medium">{camera.name}</div>
                                <div className="text-sm text-gray-400">Index: {camera.index}</div>
                              </div>
                            </div>
                            <div className={`px-2 py-1 rounded text-xs ${
                              camera.status === 'active' ? 'bg-green-400/20 text-green-400' :
                              camera.status === 'available' ? 'bg-blue-400/20 text-blue-400' :
                              'bg-red-400/20 text-red-400'
                            }`}>
                              {camera.status}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Detection Settings */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-semibold text-gray-300 mb-3">
                        Detection Threshold: {settings.detectionThreshold}
                      </label>
                      <input
                        type="range"
                        min="0.1"
                        max="1.0"
                        step="0.1"
                        value={settings.detectionThreshold}
                        onChange={(e) => handleSettingsChange('detectionThreshold', parseFloat(e.target.value))}
                        className="w-full accent-cyan-400"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-300 mb-3">
                        Max Hands: {settings.maxHands}
                      </label>
                      <input
                        type="range"
                        min="1"
                        max="4"
                        step="1"
                        value={settings.maxHands}
                        onChange={(e) => handleSettingsChange('maxHands', parseInt(e.target.value))}
                        className="w-full accent-purple-400"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-300 mb-3">
                        Resolution
                      </label>
                      <select
                        value={settings.resolution}
                        onChange={(e) => handleSettingsChange('resolution', e.target.value)}
                        className="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white focus:border-cyan-400 focus:outline-none"
                      >
                        <option value="640x480">640x480</option>
                        <option value="1280x720">1280x720 (HD)</option>
                        <option value="1920x1080">1920x1080 (FHD)</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-300 mb-3">
                        Frame Rate: {settings.fps} FPS
                      </label>
                      <input
                        type="range"
                        min="15"
                        max="60"
                        step="15"
                        value={settings.fps}
                        onChange={(e) => handleSettingsChange('fps', parseInt(e.target.value))}
                        className="w-full accent-green-400"
                      />
                    </div>
                  </div>

                  {/* Toggle Settings */}
                  <div className="flex items-center justify-between p-4 rounded-lg bg-gray-700/30 border border-gray-600">
                    <div>
                      <div className="font-medium">Safety Alarms</div>
                      <div className="text-sm text-gray-400">Enable audio alerts for emergencies</div>
                    </div>
                    <button
                      onClick={() => handleSettingsChange('alarmEnabled', !settings.alarmEnabled)}
                      className={`relative w-12 h-6 rounded-full transition-colors ${
                        settings.alarmEnabled ? 'bg-green-500' : 'bg-gray-600'
                      }`}
                    >
                      <div className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
                        settings.alarmEnabled ? 'transform translate-x-6' : ''
                      }`}></div>
                    </button>
                  </div>

                  {/* Save Button */}
                  <button
                    onClick={saveSettings}
                    className="w-full p-4 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg font-semibold hover:from-cyan-400 hover:to-blue-400 transition-all duration-300 flex items-center justify-center space-x-2"
                  >
                    <Save className="w-5 h-5" />
                    <span>Save Settings</span>
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <style>{`
        .bg-moving-grid {
          background-image: 
            linear-gradient(rgba(6, 182, 212, 0.3) 1px, transparent 1px),
            linear-gradient(90deg, rgba(6, 182, 212, 0.3) 1px, transparent 1px);
          background-size: 50px 50px;
          animation: grid-move 20s linear infinite;
        }

        @keyframes grid-move {
          0% { transform: translate(0, 0); }
          100% { transform: translate(50px, 50px); }
        }

        @keyframes float {
          0%, 100% { transform: translateY(0) rotate(0deg) scale(1); }
          25% { transform: translateY(-20px) rotate(90deg) scale(1.1); }
          50% { transform: translateY(-40px) rotate(180deg) scale(0.9); }
          75% { transform: translateY(-20px) rotate(270deg) scale(1.1); }
        }
        .animate-float { animation: float 15s ease-in-out infinite; }

        @keyframes circuit-flow {
          0% { 
            transform: translateX(-200px) rotate(var(--rotation));
            opacity: 0;
          }
          10% { opacity: 1; }
          90% { opacity: 1; }
          100% { 
            transform: translateX(200px) rotate(var(--rotation));
            opacity: 0;
          }
        }
        .animate-circuit-flow { animation: circuit-flow 8s ease-in-out infinite; }

        @keyframes data-stream {
          0% { 
            transform: translateY(-100vh);
            opacity: 0;
          }
          10% { opacity: 1; }
          90% { opacity: 1; }
          100% { 
            transform: translateY(100vh);
            opacity: 0;
          }
        }
        .animate-data-stream { animation: data-stream 15s linear infinite; }

        @keyframes particle-float {
          0%, 100% { 
            transform: translate(0, 0) scale(1);
            opacity: 0.3;
          }
          25% { 
            transform: translate(20px, -30px) scale(1.2);
            opacity: 1;
          }
          50% { 
            transform: translate(-10px, -60px) scale(0.8);
            opacity: 0.6;
          }
          75% { 
            transform: translate(-30px, -30px) scale(1.1);
            opacity: 0.9;
          }
        }
        .animate-particle-float { animation: particle-float 12s ease-in-out infinite; }

        @keyframes particle-glow {
          0%, 100% { 
            box-shadow: 0 0 5px rgba(6, 182, 212, 0.5);
            opacity: 0.4;
          }
          50% { 
            box-shadow: 0 0 20px rgba(6, 182, 212, 1), 0 0 40px rgba(6, 182, 212, 0.5);
            opacity: 1;
          }
        }
        .animate-particle-glow { animation: particle-glow 4s ease-in-out infinite; }

        @keyframes scan-vertical {
          0% { top: -2px; opacity: 1; }
          100% { top: 100%; opacity: 0; }
        }
        .animate-scan-vertical { animation: scan-vertical 8s linear infinite; }

        @keyframes scan-horizontal {
          0% { left: -2px; opacity: 1; }
          100% { left: 100%; opacity: 0; }
        }
        .animate-scan-horizontal { animation: scan-horizontal 12s linear infinite; }

        @keyframes matrix-rain {
          0% { 
            transform: translateY(-100vh);
            opacity: 0;
          }
          10% { opacity: 1; }
          90% { opacity: 1; }
          100% { 
            transform: translateY(100vh);
            opacity: 0;
          }
        }
        .animate-matrix-rain { animation: matrix-rain 12s linear infinite; }

        /* Enhanced glow effects for interactive elements */
        .group:hover .glow-effect {
          box-shadow: 0 0 30px rgba(6, 182, 212, 0.4), inset 0 0 30px rgba(6, 182, 212, 0.1);
        }

        /* Holographic border animation */
        @keyframes hologram-border {
          0%, 100% { border-color: rgba(6, 182, 212, 0.5); }
          25% { border-color: rgba(147, 51, 234, 0.5); }
          50% { border-color: rgba(34, 197, 94, 0.5); }
          75% { border-color: rgba(251, 191, 36, 0.5); }
        }
        .animate-hologram { animation: hologram-border 4s ease-in-out infinite; }
      `}</style>
    </div>
  );
};

export default ManTionApp;
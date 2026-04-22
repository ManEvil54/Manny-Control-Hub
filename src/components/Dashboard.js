import React, { useState, useEffect } from 'react';
import SystemStatus from './SystemStatus';
import BotCard from './BotCard';

/**
 * Dashboard Component
 * The main Mission Control Hub (MCH) interface.
 */
const Dashboard = () => {
  const [config, setConfig] = useState(null);
  const [botData, setBotData] = useState({
    status: 'WAITING',
    conviction_level: 'LOW',
    tier_label: 'SCOUT',
    active_symbol: 'N/A',
    last_action: 'None',
    env_mode: 'BREAKOUT',
    is_near_high: false
  });

  useEffect(() => {
    // In a real app, this would be a fetch to an API endpoint or a Firebase listener
    // For this demonstration, we'll mock the config loading
    const mockConfig = {
      active_env: 'sandbox',
      environments: {
        sandbox: { mode_label: 'PAPER TRADING' },
        production: { mode_label: 'LIVE TRADING' }
      }
    };
    setConfig(mockConfig);

    // Mock live data updates
    const timer = setTimeout(() => {
      setBotData({
        status: 'POSITION_OPEN',
        conviction_level: 'MEDIUM',
        tier_label: 'SCALING',
        active_symbol: '/MNQ',
        last_action: 'Buy',
        env_mode: 'REJECTION',
        is_near_high: true
      });
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  if (!config) return <div className="bg-black h-screen flex items-center justify-center font-mono text-neon-green text-sm tracking-widest">INITIALIZING MCH ORCHESTRATOR...</div>;

  const currentEnv = config.environments[config.active_env];

  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans selection:bg-neon-green selection:text-black">
      <SystemStatus activeEnv={config.active_env} modeLabel={currentEnv.mode_label} />
      
      <main className="max-w-6xl mx-auto p-8">
        <header className="mb-8 flex justify-between items-end">
          <div>
            <h1 className="text-4xl font-black tracking-tight mb-2">MISSION CONTROL HUB</h1>
            <p className="text-gray-500 font-mono text-[10px] tracking-widest uppercase">Autonomous Futures Trading Logic • v2.4.0</p>
          </div>
          <div className="flex flex-col items-end">
            <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${botData.is_near_high ? 'bg-red-500/10 text-red-400 border-red-500/30' : 'bg-neon-green/10 text-neon-green border-neon-green/30'} uppercase tracking-widest`}>
              {botData.is_near_high ? 'Near 52W High' : 'Range Bound'}
            </span>
            <p className="text-[9px] text-gray-600 font-mono uppercase mt-1">Nasdaq Proximity: 0.42%</p>
          </div>
        </header>

        {/* Sync-Gap-RZY Status Bar + Environment Switch */}
        <section className="mb-8 bg-black/40 border border-white/5 rounded-xl p-1 flex items-center justify-between font-mono text-[10px] tracking-widest uppercase">
          <div className="flex-1 flex items-center justify-center border-r border-white/5 py-2">
            <span className="text-gray-500 mr-2">SYNC:</span>
            <span className="text-neon-green">ACTIVE (ES/NQ)</span>
          </div>
          <div className="flex-1 flex items-center justify-center border-r border-white/5 py-2">
            <span className="text-gray-500 mr-2">GAP:</span>
            <span className="text-yellow-400">DETECTED (1M FVG)</span>
          </div>
          <div className="flex-1 flex items-center justify-center border-r border-white/5 py-2">
            <span className="text-gray-500 mr-2">RZY:</span>
            <span className="text-blue-400">MEASURING MOVE</span>
          </div>
          <div className={`flex-1 flex items-center justify-center py-2 ${botData.env_mode === 'REJECTION' ? 'bg-red-500/20' : 'bg-neon-green/20'} transition-colors duration-1000`}>
            <span className="text-gray-300 mr-2">MODE:</span>
            <span className={botData.env_mode === 'REJECTION' ? 'text-red-400 font-bold' : 'text-neon-green font-bold'}>
              {botData.env_mode} MODE
            </span>
          </div>
        </section>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1">
            <BotCard botData={botData} />
          </div>
          
          <div className="md:col-span-2 space-y-8">
            <section className="bg-white/5 border border-white/10 rounded-2xl p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xs font-mono text-gray-500 uppercase tracking-widest">Active Strategy: Little RZY</h3>
                <div className="flex gap-2">
                    <span className="text-[10px] bg-neon-green/10 text-neon-green border border-neon-green/30 px-2 py-0.5 rounded uppercase font-mono">Net Logic Active</span>
                </div>
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                <div>
                  <p className="text-2xl font-bold font-mono">15.5 <span className="text-gray-600 text-xs uppercase">Pts</span></p>
                  <p className="text-[10px] text-gray-500 uppercase font-mono mt-1">Gross Move</p>
                </div>
                <div>
                  {/* /MNQ Multiplier is $2 per point. 15.5 * 2 = $31 per contract */}
                  <p className="text-2xl font-bold font-mono text-white">$31.00</p>
                  <p className="text-[10px] text-gray-500 uppercase font-mono mt-1">Gross P&L (Per Contract)</p>
                </div>
                <div className="bg-neon-green/5 p-2 rounded-lg border border-neon-green/10">
                  {/* Net = Gross - ($0.70 * 2) = $31 - $1.40 = $29.60 */}
                  <p className="text-2xl font-bold font-mono text-neon-green">$29.60</p>
                  <p className="text-[10px] text-neon-green/60 uppercase font-mono mt-1">Net P&L (Keep)</p>
                </div>
                <div>
                  <p className="text-2xl font-bold font-mono text-white">18,245.50</p>
                  <p className="text-[10px] text-gray-500 uppercase font-mono mt-1">Measured Target</p>
                </div>
              </div>
            </section>

            <section className="bg-white/5 border border-white/10 rounded-2xl p-6">
              <h3 className="text-xs font-mono text-gray-500 uppercase mb-4 tracking-widest">Wick Defense & VWAP Sync</h3>
              <div className="flex items-center gap-12">
                <div className="flex flex-col items-center">
                    <div className="w-16 h-16 rounded-full border-4 border-neon-green flex items-center justify-center text-xs font-bold">SYNC</div>
                    <p className="text-[10px] text-gray-500 uppercase font-mono mt-2">MNQ/MES</p>
                </div>
                <div className="flex-1">
                    <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden">
                        <div className="h-full bg-neon-green w-[85%]"></div>
                    </div>
                    <div className="flex justify-between mt-2">
                        <span className="text-[10px] text-gray-500 font-mono">WICK PCT: 8%</span>
                        <span className="text-[10px] text-neon-green font-mono">VETO THRESHOLD: 15%</span>
                    </div>
                </div>
              </div>
            </section>

            {/* 1-Minute Chart FVG Visualization */}
            <section className="bg-black border border-white/10 rounded-2xl p-6 overflow-hidden relative min-h-[200px]">
              <h3 className="text-xs font-mono text-gray-500 uppercase mb-6 tracking-widest">1m Footprint Detection</h3>
              <div className="flex items-end gap-2 h-32 relative px-4">
                {/* Simulated Candles */}
                <div className="w-4 h-24 bg-red-500/30 border border-red-500/50 rounded-sm"></div>
                <div className="w-4 h-32 bg-green-500 border border-green-500/50 rounded-sm"></div>
                <div className="w-4 h-20 bg-green-500/30 border border-green-500/50 rounded-sm"></div>
                <div className="w-4 h-28 bg-green-500/30 border border-green-500/50 rounded-sm"></div>
                
                {/* FVG Box */}
                <div className="absolute left-10 bottom-12 w-32 h-16 bg-yellow-400/10 border border-dashed border-yellow-400/40 flex items-center justify-center">
                  <div className="w-full h-[1px] bg-yellow-400/30 absolute top-1/2"></div>
                  <span className="text-[8px] text-yellow-400/80 font-mono uppercase bg-black px-1 z-10">50% Golden Zone</span>
                </div>
              </div>
              <div className="mt-4 flex justify-between items-center text-[10px] font-mono text-gray-600">
                <span>09:35 AM BREAKOUT</span>
                <span className="text-yellow-400/60">FAIR VALUE GAP ACTIVE</span>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;

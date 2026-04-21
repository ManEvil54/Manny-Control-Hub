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
    last_action: 'None'
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
        last_action: 'Buy'
      });
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  if (!config) return <div className="bg-black h-screen flex items-center justify-center font-mono text-neon-green">INITIALIZING MCH...</div>;

  const currentEnv = config.environments[config.active_env];

  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans selection:bg-neon-green selection:text-black">
      <SystemStatus activeEnv={config.active_env} modeLabel={currentEnv.mode_label} />
      
      <main className="max-w-6xl mx-auto p-8">
        <header className="mb-12">
          <h1 className="text-4xl font-black tracking-tight mb-2">MISSION CONTROL HUB</h1>
          <p className="text-gray-500 font-mono text-sm tracking-widest uppercase">Autonomous Futures Trading Logic</p>
        </header>

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
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;

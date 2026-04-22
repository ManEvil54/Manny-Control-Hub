import React from 'react';
import ConvictionMeter from './ConvictionMeter';

/**
 * BotCard Component
 * Displays the status and conviction level of the Futures Sniper.
 */
const BotCard = ({ botData }) => {
  const { status, conviction_level, tier_label, active_symbol, last_action, env_mode, is_near_high } = botData;

  const getCardStyle = () => {
    if (status === 'POSITION_OPEN') {
      if (env_mode === 'REJECTION') return 'border-red-500 shadow-red-glow bg-black/80';
      return conviction_level === 'HIGH' 
        ? 'border-neon-green shadow-glow-strong animate-pulse bg-black/80' 
        : 'border-neon-green shadow-glow bg-black/60';
    }
    if (status === 'WAITING') return 'border-gray-800 grayscale opacity-50 bg-black/40';
    return 'border-gray-900 bg-black/20';
  };

  return (
    <div className={`p-6 rounded-2xl border transition-all duration-500 ${getCardStyle()}`}>
      <div className="flex justify-between items-start mb-6">
        <div>
          <h2 className="text-white font-mono text-lg tracking-tighter">FUTURES SNIPER</h2>
          <div className="flex items-center gap-2 mt-1">
            <span className={`w-2 h-2 rounded-full ${status === 'POSITION_OPEN' ? (env_mode === 'REJECTION' ? 'bg-red-500 animate-ping' : 'bg-neon-green animate-ping') : 'bg-gray-700'}`}></span>
            <p className="text-[10px] text-gray-400 font-mono uppercase tracking-widest">
              {status === 'POSITION_OPEN' ? (env_mode === 'REJECTION' ? 'High Risk Execution' : 'Live Execution') : 'Monitoring'}
            </p>
          </div>
        </div>
        {status === 'POSITION_OPEN' && (
          <div className={`${env_mode === 'REJECTION' ? 'bg-red-500/10 border-red-500/30 text-red-400' : 'bg-neon-green/10 border-neon-green/30 text-neon-green'} px-3 py-1 rounded-full border`}>
            <span className="text-[10px] font-bold font-mono">
              {tier_label}
            </span>
          </div>
        )}
      </div>

      {status === 'POSITION_OPEN' ? (
        <div className="space-y-4">
          {env_mode === 'REJECTION' && (
            <div className="bg-red-500/10 border border-red-500/30 p-3 rounded-xl">
              <p className="text-red-400 text-[9px] font-mono uppercase tracking-widest font-bold">Lance Rule: Active</p>
              <p className="text-gray-400 text-[8px] font-mono mt-1">Institutional Rejection Risk: HIGH (67% Wick Veto Enabled)</p>
            </div>
          )}
          
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white/5 p-3 rounded-xl border border-white/10">
              <p className="text-gray-500 text-[10px] uppercase font-mono mb-1">Symbol</p>
              <p className="text-white font-bold font-mono text-sm">{active_symbol}</p>
            </div>
            <div className="bg-white/5 p-3 rounded-xl border border-white/10">
              <p className="text-gray-500 text-[10px] uppercase font-mono mb-1">Action</p>
              <p className={`font-bold font-mono text-sm ${last_action === 'Buy' ? 'text-green-400' : 'text-red-400'}`}>
                {last_action}
              </p>
            </div>
          </div>
          <ConvictionMeter level={conviction_level} />
          
          <button className={`w-full py-3 rounded-xl border font-mono text-xs font-bold tracking-widest transition-all duration-300 ${
            env_mode === 'REJECTION'
              ? 'bg-red-500 text-white border-red-600 shadow-red-glow animate-pulse'
              : (conviction_level === 'HIGH' 
                  ? 'bg-neon-green text-black border-neon-green shadow-glow' 
                  : 'bg-yellow-400 text-black border-yellow-500')
          }`}>
            {env_mode === 'REJECTION' ? 'REJECTION MODE: DEFEND' : (conviction_level === 'HIGH' ? 'HAMMER: DEPLOYED' : 'HAMMER: WAITING FOR 50%')}
          </button>
        </div>
      ) : (
        <div className="py-8 text-center">
          <p className="text-gray-600 font-mono text-xs italic">Waiting for Opening Range Breakout signal...</p>
        </div>
      )}
    </div>
  );
};

export default BotCard;

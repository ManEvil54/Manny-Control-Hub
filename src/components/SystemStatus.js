import React from 'react';

/**
 * SystemStatus Component
 * Displays the current environment (Sandbox vs Production) with visual color coding.
 */
const SystemStatus = ({ activeEnv, modeLabel }) => {
  const isSandbox = activeEnv === 'sandbox';
  
  // Safety Yellow for Sandbox, Tactical Gray/Red for Production
  const statusColor = isSandbox ? 'bg-yellow-400' : 'bg-red-600';
  const textColor = isSandbox ? 'text-black' : 'text-white';
  const borderColor = isSandbox ? 'border-yellow-500' : 'border-red-700';

  return (
    <div className={`flex items-center justify-between px-4 py-2 border-b ${borderColor} ${statusColor} ${textColor} font-mono text-xs font-bold tracking-widest`}>
      <div className="flex items-center gap-4">
        <span className="flex items-center gap-2">
          <span className={`w-2 h-2 rounded-full bg-current ${isSandbox ? '' : 'animate-pulse'}`}></span>
          SYSTEM STATUS: {modeLabel}
        </span>
        <span className="opacity-60">|</span>
        <span>MCH VERSION: 2.0.26-ALPHA</span>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
            <span className="opacity-60">ACCOUNT:</span>
            <span className="underline decoration-dotted underline-offset-4 cursor-help">VA5973...</span>
        </div>
        <div className="bg-black/20 px-2 py-0.5 rounded border border-black/10 uppercase">
            {activeEnv}
        </div>
      </div>
    </div>
  );
};

export default SystemStatus;

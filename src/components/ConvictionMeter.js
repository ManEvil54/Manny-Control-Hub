import React from 'react';

/**
 * ConvictionMeter Component
 * Visualizes the current trade tier and conviction level.
 */
const ConvictionMeter = ({ level }) => {
  const getStyle = () => {
    switch (level) {
      case 'HIGH':
        return 'bg-neon-green shadow-glow animate-pulse w-full';
      case 'MEDIUM':
        return 'bg-neon-blue shadow-glow w-2/3';
      case 'LOW':
        return 'bg-gray-500 w-1/3';
      default:
        return 'bg-gray-800 w-0';
    }
  };

  return (
    <div className="mt-4">
      <div className="flex justify-between text-[10px] text-gray-500 mb-1 uppercase tracking-widest font-mono">
        <span>Conviction</span>
        <span>{level || 'None'}</span>
      </div>
      <div className="h-1 w-full bg-gray-900 rounded-full overflow-hidden">
        <div className={`h-full transition-all duration-700 ease-out ${getStyle()}`}></div>
      </div>
      {level === 'HIGH' && (
        <div className="mt-2 text-[10px] text-neon-green font-bold animate-bounce text-center uppercase">
          ★ Research Confirmed ★
        </div>
      )}
    </div>
  );
};

export default ConvictionMeter;

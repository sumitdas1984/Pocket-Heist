const HeistCardSkeleton = () => {
  return (
    <div className="bg-dark-card border border-slate-800 rounded-2xl overflow-hidden animate-pulse">
      <div className="p-6">
        {/* Status and ID */}
        <div className="flex justify-between items-start mb-4">
          <div className="h-5 w-16 bg-slate-800 rounded"></div>
          <div className="h-4 w-12 bg-slate-800 rounded"></div>
        </div>

        {/* Title */}
        <div className="h-6 w-3/4 bg-slate-800 rounded mb-2"></div>

        {/* Description */}
        <div className="space-y-2 mb-6">
          <div className="h-4 w-full bg-slate-800 rounded"></div>
          <div className="h-4 w-2/3 bg-slate-800 rounded"></div>
        </div>

        {/* Info Rows */}
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="flex justify-between items-center">
              <div className="h-3 w-20 bg-slate-800 rounded"></div>
              <div className="h-3 w-24 bg-slate-800 rounded"></div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="bg-slate-900/50 p-4 border-t border-slate-800 flex justify-between items-center">
        <div className="h-4 w-24 bg-slate-800 rounded"></div>
        <div className="h-4 w-16 bg-slate-800 rounded"></div>
      </div>
    </div>
  );
};

export default HeistCardSkeleton;

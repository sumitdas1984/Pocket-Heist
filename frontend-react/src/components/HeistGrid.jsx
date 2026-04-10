import HeistCard from './HeistCard';

const HeistGrid = ({ heists, onAbort, currentUsername, emptyMessage = 'No heists found.' }) => {
  if (!heists || heists.length === 0) {
    return (
      <div className="text-center py-16">
        <div className="text-6xl mb-4">📭</div>
        <p className="text-slate-400 text-lg">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {heists.map((heist) => (
        <HeistCard
          key={heist.id}
          heist={heist}
          onAbort={onAbort}
          currentUsername={currentUsername}
        />
      ))}
    </div>
  );
};

export default HeistGrid;

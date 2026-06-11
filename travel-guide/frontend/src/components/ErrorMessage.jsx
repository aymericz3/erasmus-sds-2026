export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="status-message error-message" role="alert">
      <p>{message}</p>
      {onRetry && (
        <button className="secondary" onClick={onRetry}>
          Retry
        </button>
      )}
    </div>
  );
}

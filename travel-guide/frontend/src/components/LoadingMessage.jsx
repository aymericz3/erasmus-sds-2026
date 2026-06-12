export default function LoadingMessage({ message = "Loading attractions..." }) {
  return <div className="status-message loading-message">{message}</div>;
}

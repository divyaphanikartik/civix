import { useHotspots } from "../hooks/useHotspots";
import HotspotMap from "../components/map/HotspotMap";
import HotspotList from "../components/hotspots/HotspotList";


export default function Dashboard() {

  const {
    hotspots,
    loading,
    error
  } = useHotspots();


  if (loading) {
    return <div>Loading Civix...</div>;
  }


  if (error) {
    return (
      <div>
        Failed to load hotspots.
      </div>
    );
  }


  return (

    <div className="dashboard">

      <header>
        <h1>Civix</h1>

        <p>
          Infrastructure Decision
          Cockpit
        </p>
      </header>


      <section className="dashboard-grid">

        <HotspotMap
          hotspots={hotspots}
        />

        <HotspotList
          hotspots={hotspots}
        />

      </section>

    </div>

  );
}
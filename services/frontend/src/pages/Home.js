import HomeSideBarLeft from "../components/HomeSideBarLeft";
import HomeSideBarRight from "../components/HomeSideBarRight";
import HomeGraph from "../components/HomeGraph";
import "./Home.css";
import SideDropDown from "../components/SideDropDown";
import SideDropDownCheckbox from "../components/SideDropDownCheckbox";
import SideDropDownRadio from "../components/SideDropDownRadio";
import EditStationsWindow from "../components/EditStationsWindow";
import React, { useEffect, useState } from "react";
import HomeButton from "../components/HomeButton";
import { config } from "../Constants";

const Home = () => {
  const [timePeriods, setTimePeriod] = useState({
    "6hr": true,
    "12hr": false,
    "24hr": false,
    "48hr": false,
    "5day": false,
    "10day": false,
    "1month": false,
  });
  const [stations, setStations] = useState([]);
  const [tempStations, setTempStations] = useState(null);
  const [leftSideBarVisible, setLeftSideBarVisible] = useState(true);
  const [stationDropVisible, setStationDropVisible] = useState(true);
  const [editStationPopupVisible, setEditStationPopupVisible] = useState(false);
  const [timeDropVisible, setTimeDropVisible] = useState(true);
  const [zipcode, setZipcode] = useState("11206");
  const [zipQuery, setZipQuery] = useState("11206");
  const [rawReadings, setRawReadings] = useState({});
  const [dates, setDates] = useState([]);
  const [aqiData, setAqiData] = useState([]);
  const [idsToGraph, setIdsToGraph] = useState([""]);

  const toggleSideBar = () => {
    setLeftSideBarVisible(!leftSideBarVisible);
  };

  const toggleStationDrop = () => {
    setStationDropVisible(!stationDropVisible);
  };

  const toggleTimeDrop = () => {
    setTimeDropVisible(!timeDropVisible);
  };

  const toggleEditStationPopup = () => {
    setEditStationPopupVisible(!editStationPopupVisible);
  };

  const handleZipcodeChange = (e) => {
    setZipcode(e.target.value);
  };

  const handleZipQueryChange = () => {
    setZipQuery(zipcode);
  };

  const pickTimePeriod = (e) => {
    const newPeriods = {};
    for (const key of Object.keys(timePeriods)) {
      key === e.target.name
        ? (newPeriods[key] = true)
        : (newPeriods[key] = false);
    }
    setTimePeriod(newPeriods);
  };

  const updateStations = (e) => {
    e.preventDefault();
    const trueStations = tempStations.map((station) =>
      station["checked"] === true
        ? {
            station_id: station["station_id"],
            station_name: station["station_name"],
            checked: true,
            latitude: station["latitude"],
            longitude: station["longitude"],
            location_coord: station["location_coord"],
          }
        : null
    );
    const newStations = trueStations.filter(Boolean);
    setStations(newStations);
    toggleEditStationPopup();
  };

  const updateIds = () => {
    const newIds = [];
    stations.forEach((station) => {
      if (station["checked"]) {
        newIds.push(station["station_id"]);
      }
    });
    setIdsToGraph(newIds);
  };

  const handleStationCheckChange = (e) => {
    const updatedStations = [...stations];
    updatedStations.forEach((station) => {
      if (station["station_id"] === e.target.name) {
        station["checked"] = !station["checked"];
      }
    });
    setStations(updatedStations);
  };

  const handleTempCheckChange = (e) => {
    const updatedTempStations = [...tempStations];
    updatedTempStations.forEach((station) => {
      if (station["station_id"] === e.target.name) {
        station["checked"] = !station["checked"];
      }
    });
    setTempStations(updatedTempStations);
  };

  // const getTempStationPollutants = async (stationIDs) => {
  //   const response = await fetch(`${config.urls.READINGS_URL}${stationID}`, {
  //     mode: "cors",
  //   })
  //   let pollutants = {}
  //   return
  // }

  useEffect(() => {
    const findStations = async () => {
      const response = await fetch(`${config.urls.STATIONS_URL}${zipcode}`, {
        mode: "cors",
      });

      const data = await response.json();
      const tempArr = [...data, ...stations];
      const tempArrTwo = tempArr.filter(
        (value, index, arr) =>
          index ===
          arr.findIndex((item) => item["station_id"] === value["station_id"])
      );
      tempArrTwo.forEach((station) => (station["checked"] = false));

      setTempStations(tempArrTwo);
    };

    findStations();
  }, [zipQuery]);

  const getReadings = async (ids) => {
    let qParam = ids.reduce((prev, id) => prev + `ids=${id}&`, "?");
    if (qParam.slice(-1) === "&") {
      qParam = qParam.slice(0, -1);
    }

    const response = await fetch(`${config.urls.READINGS_URL}${qParam}`);
    const data = await response.json();
    console.log("data[0]");
    console.log(data[0]);

    return data;
  };

  // const getTempStationPollutants = async () => {
  //   const ids = tempStations.map(station => station["station_id"])
  //   const data = await getReadings(ids)
  //   const pollutants = data.map((station) => {
  //     const plts = {station["station_id"]: []}
  //     for (const [key, value] of Object.entries(station["ReadingsAirnow"])) {
  //       if (value != null && key.slice(-3) == "aqi") {
  //         plts[station["station_id"]].push(key.slice(0, -3))
  //       }
  //     }
  //   })
  // }
  const handleReadingDataChange = async () => {
    const data = await getReadings(idsToGraph);
    const dates = []
    for (const [key, value] of Object.entries(data[0])) {
      for 
    }
    const dates = data[0].map(
      (reading) => reading["ReadingsAirnow"]["reading_datetime"]
    );

    const aqiData = data.map((station) => ({
      station_id: station[0]["ReadingsAirnow"]["station_id"],
      data: station.map((reading) => reading["ReadingsAirnow"]["pm25_aqi"]),
    }));

    setRawReadings(data);
    setDates(dates);
    setAqiData(aqiData);
  };

  useEffect(() => {
    handleReadingDataChange();
  }, [idsToGraph]);

  return (
    <div className="dashboard-container">
      <HomeSideBarLeft
        toggleSideBar={toggleSideBar}
        contentVisible={leftSideBarVisible}
      >
        {editStationPopupVisible ? (
          <EditStationsWindow
            zipcode={zipcode}
            setZipcode={setZipcode}
            tempStations={tempStations}
            updateStations={updateStations}
            handleTempCheckChange={handleTempCheckChange}
            handleZipcodeChange={handleZipcodeChange}
            handleZipQueryChange={handleZipQueryChange}
          />
        ) : null}
        <SideDropDown
          name={"stations"}
          onClick={toggleStationDrop}
          contentVisible={stationDropVisible}
        >
          {stations.map((station) => (
            <SideDropDownCheckbox
              key={station["station_id"]}
              name={station["station_id"]}
              value={station["station_name"]}
              checked={station["checked"]}
              onChange={handleStationCheckChange}
            />
          ))}
          <HomeButton
            onClick={toggleEditStationPopup}
            value={"add/remove stations"}
          />
        </SideDropDown>

        <SideDropDown
          name={"time period"}
          onClick={toggleTimeDrop}
          contentVisible={timeDropVisible}
          hasBtn={false}
        >
          {Object.entries(timePeriods).map((item) => (
            <SideDropDownRadio
              key={item[0]}
              name={item[0]}
              checked={item[1]}
              onChange={pickTimePeriod}
            />
          ))}
        </SideDropDown>
        <HomeButton onClick={updateIds} value={"update graph"} />
      </HomeSideBarLeft>

      <HomeGraph dates={dates} aqiData={aqiData} />

      <HomeSideBarRight />
    </div>
  );
};

export default Home;

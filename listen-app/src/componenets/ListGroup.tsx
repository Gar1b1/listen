import React, { useState } from "react";

interface ListItem {
  id: number;
  label: string;
}

interface Props {
  items: ListItem[];
  heading: string;
  renderRight?: (item: ListItem, index: number) => React.ReactNode;
}

function ListGroup({ items, heading, renderRight }: Props) {
  const [selectedIndex, setSelectedIndex] = useState(-1);

  const listItemStyle: React.CSSProperties = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    cursor: "pointer",
    padding: "0.5rem 1rem",
    border: "1px solid #ddd",
    marginBottom: "4px",
    borderRadius: "4px",
  };

  const activeStyle: React.CSSProperties = {
    backgroundColor: "#0d6efd",
    color: "white",
  };

  // Add this container style to wrap buttons with gap
  const rightButtonsContainerStyle: React.CSSProperties = {
    display: "flex",
    gap: "8px",
  };

  return (
    <>
      <h1>{heading}</h1>
      {items.length === 0 && <p>No Songs Found</p>}
      <ul style={{ listStyleType: "none", padding: 0 }}>
        {items.map((item, index) => (
          <li
            key={item.id}
            style={{
              ...listItemStyle,
              ...(selectedIndex === index ? activeStyle : {}),
            }}
            onClick={() => setSelectedIndex(index)}
          >
            <span>{item.label}</span>
            <div style={rightButtonsContainerStyle}>
              {renderRight?.(item, index)}
            </div>
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;

from datetime import datetime, timezone

from fastapi import APIRouter, Query

from app.database import get_db_connection, row_to_dict
from app.models import NbiotPacket


router = APIRouter()


@router.post("/nbiot")
def receive_nbiot_packet(packet: NbiotPacket):
    received_at = datetime.now(timezone.utc).isoformat()

    connection = get_db_connection()

    cursor = connection.execute(
        """
        INSERT INTO nbiot_packets (payload, ip, port, received_at)
        VALUES (?, ?, ?, ?)
        """,
        (packet.payload, packet.ip, packet.port, received_at)
    )

    connection.commit()
    packet_id = cursor.lastrowid
    connection.close()

    saved_packet = {
        "id": packet_id,
        "payload": packet.payload,
        "ip": packet.ip,
        "port": packet.port,
        "received_at": received_at
    }

    return {
        "status": "received",
        "command": "CALL_FN",
        "data": saved_packet
    }


@router.get("/latest")
def get_latest_packet():
    connection = get_db_connection()

    row = connection.execute(
        """
        SELECT id, payload, ip, port, received_at
        FROM nbiot_packets
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    connection.close()

    latest_packet = row_to_dict(row)

    if latest_packet is None:
        return {
            "message": "No NB-IoT packet received yet"
        }

    return latest_packet


@router.get("/history")
def get_packet_history(
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0)
):
    connection = get_db_connection()

    total_row = connection.execute(
        "SELECT COUNT(*) FROM nbiot_packets"
    ).fetchone()

    rows = connection.execute(
        """
        SELECT id, payload, ip, port, received_at
        FROM nbiot_packets
        ORDER BY id DESC
        LIMIT ? OFFSET ?
        """,
        (limit, offset)
    ).fetchall()

    connection.close()

    packets = [row_to_dict(row) for row in rows]

    return {
        "total": total_row[0],
        "limit": limit,
        "offset": offset,
        "data": packets
    }


@router.get("/count")
def get_packet_count():
    connection = get_db_connection()

    row = connection.execute(
        "SELECT COUNT(*) FROM nbiot_packets"
    ).fetchone()

    connection.close()

    return {
        "total_packets": row[0]
    }


@router.get("/packets/{packet_id}")
def get_packet_by_id(packet_id: int):
    connection = get_db_connection()

    row = connection.execute(
        """
        SELECT id, payload, ip, port, received_at
        FROM nbiot_packets
        WHERE id = ?
        """,
        (packet_id,)
    ).fetchone()

    connection.close()

    packet = row_to_dict(row)

    if packet is None:
        return {
            "message": f"No packet found with id {packet_id}"
        }

    return packet


@router.get("/history/by-ip")
def get_packets_by_ip(
    ip: str,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0)
):
    ip = ip.strip()

    connection = get_db_connection()

    total_row = connection.execute(
        """
        SELECT COUNT(*)
        FROM nbiot_packets
        WHERE TRIM(ip) = ?
        """,
        (ip,)
    ).fetchone()

    rows = connection.execute(
        """
        SELECT id, payload, ip, port, received_at
        FROM nbiot_packets
        WHERE TRIM(ip) = ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
        """,
        (ip, limit, offset)
    ).fetchall()

    connection.close()

    packets = [row_to_dict(row) for row in rows]

    return {
        "ip": ip,
        "total": total_row[0],
        "limit": limit,
        "offset": offset,
        "data": packets
    }


@router.get("/history/search")
def search_packet_payload(
    keyword: str,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0)
):
    keyword = keyword.strip()
    search_pattern = f"%{keyword}%"

    connection = get_db_connection()

    total_row = connection.execute(
        """
        SELECT COUNT(*)
        FROM nbiot_packets
        WHERE payload LIKE ?
        """,
        (search_pattern,)
    ).fetchone()

    rows = connection.execute(
        """
        SELECT id, payload, ip, port, received_at
        FROM nbiot_packets
        WHERE payload LIKE ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
        """,
        (search_pattern, limit, offset)
    ).fetchall()

    connection.close()

    packets = [row_to_dict(row) for row in rows]

    return {
        "keyword": keyword,
        "total": total_row[0],
        "limit": limit,
        "offset": offset,
        "data": packets
    }


@router.get("/devices")
def get_unique_devices():
    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT ip, COUNT(*) AS packet_count
        FROM nbiot_packets
        WHERE ip IS NOT NULL
        GROUP BY ip
        ORDER BY packet_count DESC
        """
    ).fetchall()

    connection.close()

    devices = [
        {
            "ip": row["ip"],
            "packet_count": row["packet_count"]
        }
        for row in rows
    ]

    return {
        "total_devices": len(devices),
        "devices": devices
    }


@router.delete("/history")
def clear_packet_history():
    connection = get_db_connection()

    connection.execute("DELETE FROM nbiot_packets")
    connection.commit()
    connection.close()

    return {
        "status": "cleared",
        "message": "All packet history has been removed from database"
    }


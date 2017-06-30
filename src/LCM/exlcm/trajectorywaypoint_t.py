"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class trajectorywaypoint_t(object):
    __slots__ = ["x_cm", "y_cm", "phi", "v_mmps", "curve", "east_cm", "north_cm", "left_tol_cm", "right_tol_cm"]

    def __init__(self):
        self.x_cm = 0
        self.y_cm = 0
        self.phi = 0
        self.v_mmps = 0
        self.curve = 0
        self.east_cm = 0
        self.north_cm = 0
        self.left_tol_cm = 0
        self.right_tol_cm = 0

    def encode(self):
        buf = BytesIO()
        buf.write(trajectorywaypoint_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">hhhhhhhbb", self.x_cm, self.y_cm, self.phi, self.v_mmps, self.curve, self.east_cm, self.north_cm, self.left_tol_cm, self.right_tol_cm))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != trajectorywaypoint_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return trajectorywaypoint_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = trajectorywaypoint_t()
        self.x_cm, self.y_cm, self.phi, self.v_mmps, self.curve, self.east_cm, self.north_cm, self.left_tol_cm, self.right_tol_cm = struct.unpack(">hhhhhhhbb", buf.read(16))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if trajectorywaypoint_t in parents: return 0
        tmphash = (0x3f8d01b152327726) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if trajectorywaypoint_t._packed_fingerprint is None:
            trajectorywaypoint_t._packed_fingerprint = struct.pack(">Q", trajectorywaypoint_t._get_hash_recursive([]))
        return trajectorywaypoint_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

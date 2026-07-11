# NAVIGATION_ENGINE_ARCHITECTURE.md

## Chapter 3 — Rendering Architecture

### Goal

Build a smooth, mobile-first, interactive 3D stadium.

---

## Stack

* React Three Fiber
* Three.js
* @react-three/drei
* react-spring (minimal)
* GLTF
* Draco Compression
* KTX2 Textures

---

## Scene

```
World
 ├── Sky
 ├── Stadium
 ├── Parking
 ├── Roads
 ├── Gates
 ├── Levels
 ├── Seats
 ├── Facilities
 ├── Route Layer
 ├── Crowd Layer
 ├── AI Layer
 └── Camera
```

---

## Camera Modes

* Explore
* Navigation
* Follow Path
* Overview
* Emergency

---

## Rendering Rules

* InstancedMesh for seats
* LOD for stadium
* Lazy load levels
* Frustum culling
* Shadow only where needed
* No >2K textures

---

## Performance Budget

FPS

* Mobile: 45+
* Desktop: 60+

Draw Calls

<150

Triangles

<800k

Texture Memory

<150MB

---

## User Interaction

Tap

↓

Highlight

↓

Metadata Popup

↓

Navigate

Long Press

↓

Context Menu

Pinch

↓

Zoom

Drag

↓

Rotate

---

## Path Animation

```
Node

↓

Glow

↓

Spline grows

↓

Next Node

↓

Destination

↓

Zoom Out
```

---

## Colors

Green

Optimal

Blue

Normal

Yellow

Busy

Red

Congested

Gold

Destination

Purple

VIP

Cyan

Accessible

---

## Done

* 60 FPS desktop
* 45 FPS mobile
* Smooth zoom
* Smooth rotation
* Path animation
* Stable camera
* No flicker

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import (QPainter, QColor, QPen, QBrush, QFont, QLinearGradient, 
                         QRadialGradient, QPainterPath, QPixmap, QFontMetrics)
import random
import math
import time
import numpy as np

class CyberpunkHackerBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # type: ignore
        
        # Core animation properties
        self.time = 0
        self.frame_count = 0
        
        # Matrix rain system
        self.matrix_drops = []
        self.matrix_chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        self.matrix_colors = [
            QColor(0, 255, 180),    # Cyan green
            QColor(0, 255, 255),    # Cyan
            QColor(255, 0, 255),    # Magenta
            QColor(57, 255, 20),    # Bright green
            QColor(255, 255, 0),    # Yellow
        ]
        
        # Neural network nodes
        self.neural_nodes = []
        self.neural_connections = []
        self.synaptic_firings = []
        
        # Data streams
        self.data_streams = []
        self.binary_rain = []
        
        # Glitch effects
        self.glitch_lines = []
        self.glitch_blocks = []
        self.glitch_timer = 0
        
        # Holographic elements
        self.hologram_rings = []
        self.hologram_texts = []
        self.hologram_particles = []
        
        # Scanning effects
        self.scan_lines = []
        self.radar_sweeps = []
        self.security_grid = []
        
        # Particle systems
        self.energy_particles = []
        self.digital_dust = []
        self.neon_trails = []
        
        # Audio visualization (simulated)
        self.audio_spectrum = []
        self.bass_drops = []
        
        # Initialize all systems
        self.init_matrix_rain()
        self.init_neural_network()
        self.init_data_streams()
        self.init_glitch_effects()
        self.init_holographic_elements()
        self.init_scanning_effects()
        self.init_particle_systems()
        self.init_audio_visualization()
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS for smooth animation
        
    def init_matrix_rain(self):
        """Initialize the Matrix-style digital rain effect"""
        cols = max(1, self.width() // 15)
        for _ in range(cols):
            self.matrix_drops.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(-self.height(), 0),
                'speed': random.uniform(3, 12),
                'length': random.randint(8, 25),
                'chars': [random.choice(self.matrix_chars) for _ in range(random.randint(8, 20))],
                'color': random.choice(self.matrix_colors),
                'brightness': random.uniform(0.3, 1.0),
                'fade_speed': random.uniform(0.02, 0.08),
                'glow': random.uniform(0, 1)
            })

    def init_neural_network(self):
        """Initialize neural network visualization"""
        node_count = 35
        for _ in range(node_count):
            node = {
                'x': random.randint(50, max(51, self.width()-50)),
                'y': random.randint(50, max(51, self.height()-50)),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'size': random.randint(3, 8),
                'energy': random.uniform(0, 1),
                'connections': [],
                'pulse': random.uniform(0, 2*math.pi),
                'type': random.choice(['input', 'hidden', 'output', 'gateway'])
            }
            self.neural_nodes.append(node)
        
        # Create connections between nearby nodes
        for i, node in enumerate(self.neural_nodes):
            for j, other in enumerate(self.neural_nodes):
                if i != j:
                    dist = math.sqrt((node['x'] - other['x'])**2 + (node['y'] - other['y'])**2)
                    if dist < 150 and random.random() < 0.3:
                        node['connections'].append(j)

    def init_data_streams(self):
        """Initialize flowing data streams"""
        for _ in range(12):
            stream = {
                'start_x': random.randint(0, self.width()),
                'start_y': random.randint(0, self.height()),
                'end_x': random.randint(0, self.width()),
                'end_y': random.randint(0, self.height()),
                'progress': random.uniform(0, 1),
                'speed': random.uniform(0.005, 0.02),
                'data': [random.choice('01') for _ in range(random.randint(20, 50))],
                'color': random.choice(self.matrix_colors),
                'width': random.randint(1, 3),
                'glow': random.uniform(0.5, 1.0)
            }
            self.data_streams.append(stream)

    def init_glitch_effects(self):
        """Initialize glitch and corruption effects"""
        for _ in range(8):
            self.glitch_lines.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'width': random.randint(2, 8),
                'height': random.randint(10, 50),
                'color': QColor(255, 0, 255, random.randint(100, 200)),
                'life': random.randint(10, 30),
                'max_life': random.randint(10, 30)
            })

        for _ in range(15):
            self.glitch_blocks.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'size': random.randint(5, 20),
                'color': QColor(0, 255, 255, random.randint(80, 150)),
                'life': random.randint(5, 15),
                'max_life': random.randint(5, 15)
            })

    def init_holographic_elements(self):
        """Initialize holographic UI elements"""
        # Holographic rings
        for _ in range(6):
            ring = {
                'center_x': random.randint(100, max(101, self.width()-100)),
                'center_y': random.randint(100, max(101, self.height()-100)),
                'radius': random.randint(30, 80),
                'thickness': random.randint(2, 6),
                'rotation': random.uniform(0, 2*math.pi),
                'rotation_speed': random.uniform(-0.02, 0.02),
                'color': random.choice(self.matrix_colors),
                'alpha': random.randint(80, 180),
                'pulse': random.uniform(0, 2*math.pi)
            }
            self.hologram_rings.append(ring)
        
        # Holographic text
        hologram_texts = [
            "SYSTEM ONLINE", "NEURAL LINK ACTIVE", "QUANTUM PROCESSING",
            "CYBERNETIC INTERFACE", "DIGITAL CONSCIOUSNESS", "VIRTUAL REALITY",
            "HACKER PROTOCOL", "SECURITY BYPASS", "DATA STREAM",
            "NEURAL NETWORK", "QUANTUM ENCRYPTION", "CYBERSPACE"
        ]
        
        for _ in range(8):
            text = {
                'text': random.choice(hologram_texts),
                'x': random.randint(50, max(51, self.width()-200)),
                'y': random.randint(50, max(51, self.height()-50)),
                'alpha': random.randint(40, 120),
                'scale': random.uniform(0.8, 1.2),
                'rotation': random.uniform(-0.1, 0.1),
                'color': random.choice(self.matrix_colors),
                'glitch': random.uniform(0, 1),
                'life': random.randint(100, 300)
            }
            self.hologram_texts.append(text)

    def init_scanning_effects(self):
        """Initialize scanning and security effects"""
        # Scan lines
        for _ in range(5):
            scan = {
                'y': random.randint(0, self.height()),
                'width': self.width(),
                'height': random.randint(1, 3),
                'speed': random.uniform(1, 3),
                'direction': random.choice([-1, 1]),
                'color': QColor(0, 255, 255, 120),
                'glow': random.uniform(0.5, 1.0)
            }
            self.scan_lines.append(scan)
        
        # Radar sweeps
        for _ in range(3):
            radar = {
                'center_x': random.randint(100, max(101, self.width()-100)),
                'center_y': random.randint(100, max(101, self.height()-100)),
                'radius': random.randint(50, 120),
                'angle': random.uniform(0, 2*math.pi),
                'speed': random.uniform(0.02, 0.05),
                'color': QColor(255, 255, 0, 100),
                'thickness': random.randint(2, 5)
            }
            self.radar_sweeps.append(radar)

    def init_particle_systems(self):
        """Initialize particle effects"""
        # Energy particles
        for _ in range(100):
            particle = {
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'size': random.randint(1, 4),
                'life': random.randint(50, 200),
                'max_life': random.randint(50, 200),
                'color': random.choice(self.matrix_colors),
                'alpha': random.randint(100, 255)
            }
            self.energy_particles.append(particle)
        
        # Digital dust
        for _ in range(150):
            dust = {
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 3),
                'life': random.randint(100, 300),
                'max_life': random.randint(100, 300),
                'color': QColor(0, 255, 255, random.randint(30, 80))
            }
            self.digital_dust.append(dust)

    def init_audio_visualization(self):
        """Initialize simulated audio visualization"""
        self.audio_spectrum = [random.uniform(0, 1) for _ in range(64)]
        for _ in range(8):
            self.bass_drops.append({
                'x': random.randint(0, self.width()),
                'y': self.height(),
                'vy': random.uniform(-8, -3),
                'size': random.randint(5, 15),
                'life': random.randint(20, 60),
                'color': QColor(255, 0, 255, random.randint(100, 200))
            })

    def animate(self):
        """Main animation loop"""
        self.time += 0.016  # 16ms per frame
        self.frame_count += 1
        
        # Update all animation systems
        self.animate_matrix_rain()
        self.animate_neural_network()
        self.animate_data_streams()
        self.animate_glitch_effects()
        self.animate_holographic_elements()
        self.animate_scanning_effects()
        self.animate_particle_systems()
        self.animate_audio_visualization()
        
        self.update()

    def animate_matrix_rain(self):
        """Animate Matrix digital rain"""
        for drop in self.matrix_drops:
            drop['y'] += drop['speed']
            drop['glow'] = (math.sin(self.time * 2 + drop['x'] * 0.01) + 1) * 0.5
            
            # Reset drop when it goes off screen
            if drop['y'] > self.height() + 100:
                drop['y'] = random.randint(-100, -20)
                drop['x'] = random.randint(0, self.width())
                drop['chars'] = [random.choice(self.matrix_chars) for _ in range(random.randint(8, 20))]
                drop['color'] = random.choice(self.matrix_colors)

    def animate_neural_network(self):
        """Animate neural network nodes and connections"""
        for node in self.neural_nodes:
            # Update position
            node['x'] += node['vx']
            node['y'] += node['vy']
            
            # Bounce off walls
            if node['x'] < 20 or node['x'] > self.width() - 20:
                node['vx'] *= -1
            if node['y'] < 20 or node['y'] > self.height() - 20:
                node['vy'] *= -1
            
            # Update energy and pulse
            node['energy'] = (math.sin(self.time + node['x'] * 0.01) + 1) * 0.5
            node['pulse'] += 0.05
            
            # Random synaptic firing
            if random.random() < 0.01:
                self.synaptic_firings.append({
                    'node': node,
                    'life': 20,
                    'max_life': 20,
                    'color': random.choice(self.matrix_colors)
                })

    def animate_data_streams(self):
        """Animate flowing data streams"""
        for stream in self.data_streams:
            stream['progress'] += stream['speed']
            if stream['progress'] >= 1:
                stream['progress'] = 0
                stream['start_x'] = random.randint(0, self.width())
                stream['start_y'] = random.randint(0, self.height())
                stream['end_x'] = random.randint(0, self.width())
                stream['end_y'] = random.randint(0, self.height())
                stream['data'] = [random.choice('01') for _ in range(random.randint(20, 50))]

    def animate_glitch_effects(self):
        """Animate glitch and corruption effects"""
        self.glitch_timer += 1
        
        # Update glitch lines
        for line in self.glitch_lines[:]:
            line['life'] -= 1
            if line['life'] <= 0:
                self.glitch_lines.remove(line)
                # Create new glitch line
                self.glitch_lines.append({
                    'x': random.randint(0, self.width()),
                    'y': random.randint(0, self.height()),
                    'width': random.randint(2, 8),
                    'height': random.randint(10, 50),
                    'color': QColor(255, 0, 255, random.randint(100, 200)),
                    'life': random.randint(10, 30),
                    'max_life': random.randint(10, 30)
                })
        
        # Update glitch blocks
        for block in self.glitch_blocks[:]:
            block['life'] -= 1
            if block['life'] <= 0:
                self.glitch_blocks.remove(block)
                # Create new glitch block
                self.glitch_blocks.append({
                    'x': random.randint(0, self.width()),
                    'y': random.randint(0, self.height()),
                    'size': random.randint(5, 20),
                    'color': QColor(0, 255, 255, random.randint(80, 150)),
                    'life': random.randint(5, 15),
                    'max_life': random.randint(5, 15)
                })

    def animate_holographic_elements(self):
        """Animate holographic UI elements"""
        # Update holographic rings
        for ring in self.hologram_rings:
            ring['rotation'] += ring['rotation_speed']
            ring['pulse'] += 0.03
        
        # Update holographic texts
        for text in self.hologram_texts[:]:
            text['life'] -= 1
            text['glitch'] = random.uniform(0, 1) if random.random() < 0.1 else text['glitch']
            
            if text['life'] <= 0:
                self.hologram_texts.remove(text)
                # Create new holographic text
                hologram_texts = [
                    "SYSTEM ONLINE", "NEURAL LINK ACTIVE", "QUANTUM PROCESSING",
                    "CYBERNETIC INTERFACE", "DIGITAL CONSCIOUSNESS", "VIRTUAL REALITY",
                    "HACKER PROTOCOL", "SECURITY BYPASS", "DATA STREAM",
                    "NEURAL NETWORK", "QUANTUM ENCRYPTION", "CYBERSPACE"
                ]
                self.hologram_texts.append({
                    'text': random.choice(hologram_texts),
                    'x': random.randint(50, max(51, self.width()-200)),
                    'y': random.randint(50, max(51, self.height()-50)),
                    'alpha': random.randint(40, 120),
                    'scale': random.uniform(0.8, 1.2),
                    'rotation': random.uniform(-0.1, 0.1),
                    'color': random.choice(self.matrix_colors),
                    'glitch': random.uniform(0, 1),
                    'life': random.randint(100, 300)
                })

    def animate_scanning_effects(self):
        """Animate scanning and security effects"""
        # Update scan lines
        for scan in self.scan_lines:
            scan['y'] += scan['speed'] * scan['direction']
            if scan['y'] < 0 or scan['y'] > self.height():
                scan['direction'] *= -1
                scan['y'] = max(0, min(scan['y'], self.height()))
        
        # Update radar sweeps
        for radar in self.radar_sweeps:
            radar['angle'] += radar['speed']

    def animate_particle_systems(self):
        """Animate particle effects"""
        # Update energy particles
        for particle in self.energy_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            # Bounce off walls
            if particle['x'] < 0 or particle['x'] > self.width():
                particle['vx'] *= -1
            if particle['y'] < 0 or particle['y'] > self.height():
                particle['vy'] *= -1
            
            if particle['life'] <= 0:
                self.energy_particles.remove(particle)
                # Create new particle
                self.energy_particles.append({
                    'x': random.randint(0, self.width()),
                    'y': random.randint(0, self.height()),
                    'vx': random.uniform(-2, 2),
                    'vy': random.uniform(-2, 2),
                    'size': random.randint(1, 4),
                    'life': random.randint(50, 200),
                    'max_life': random.randint(50, 200),
                    'color': random.choice(self.matrix_colors),
                    'alpha': random.randint(100, 255)
                })
        
        # Update digital dust
        for dust in self.digital_dust[:]:
            dust['x'] += dust['vx']
            dust['y'] += dust['vy']
            dust['life'] -= 1
            
            if dust['life'] <= 0:
                self.digital_dust.remove(dust)
                # Create new dust particle
                self.digital_dust.append({
                    'x': random.randint(0, self.width()),
                    'y': random.randint(0, self.height()),
                    'vx': random.uniform(-0.5, 0.5),
                    'vy': random.uniform(-0.5, 0.5),
                    'size': random.randint(1, 3),
                    'life': random.randint(100, 300),
                    'max_life': random.randint(100, 300),
                    'color': QColor(0, 255, 255, random.randint(30, 80))
                })

    def animate_audio_visualization(self):
        """Animate simulated audio visualization"""
        # Simulate audio spectrum
        for i in range(len(self.audio_spectrum)):
            self.audio_spectrum[i] = max(0, self.audio_spectrum[i] + random.uniform(-0.1, 0.1))
            self.audio_spectrum[i] = min(1, self.audio_spectrum[i])
        
        # Update bass drops
        for drop in self.bass_drops[:]:
            drop['y'] += drop['vy']
            drop['life'] -= 1
            
            if drop['life'] <= 0 or drop['y'] < -50:
                self.bass_drops.remove(drop)
                # Create new bass drop
                self.bass_drops.append({
                    'x': random.randint(0, self.width()),
                    'y': self.height(),
                    'vy': random.uniform(-8, -3),
                    'size': random.randint(5, 15),
                    'life': random.randint(20, 60),
                    'color': QColor(255, 0, 255, random.randint(100, 200))
                })

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create dark gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(5, 5, 15))
        gradient.setColorAt(0.5, QColor(10, 10, 25))
        gradient.setColorAt(1, QColor(0, 0, 10))
        painter.fillRect(self.rect(), gradient)
        
        # Draw all animation layers
        self.paint_matrix_rain(painter)
        self.paint_neural_network(painter)
        self.paint_data_streams(painter)
        self.paint_glitch_effects(painter)
        self.paint_holographic_elements(painter)
        self.paint_scanning_effects(painter)
        self.paint_particle_systems(painter)
        self.paint_audio_visualization(painter)

    def paint_matrix_rain(self, painter):
        """Paint Matrix digital rain effect"""
        font = QFont("Consolas", 12)
        painter.setFont(font)
        
        for drop in self.matrix_drops:
            color = drop['color']
            alpha = int(255 * drop['brightness'] * drop['glow'])
            color.setAlpha(alpha)
            painter.setPen(QPen(color, 1))
            
            for i, char in enumerate(drop['chars']):
                y = drop['y'] - i * 15
                if 0 <= y <= self.height():
                    painter.drawText(int(drop['x']), int(y), char)

    def paint_neural_network(self, painter):
        """Paint neural network visualization"""
        # Draw connections
        for node in self.neural_nodes:
            for conn_idx in node['connections']:
                if conn_idx < len(self.neural_nodes):
                    other = self.neural_nodes[conn_idx]
                    dist = math.sqrt((node['x'] - other['x'])**2 + (node['y'] - other['y'])**2)
                    if dist < 200:
                        alpha = int(100 * (1 - dist/200))
                        color = QColor(0, 255, 255, alpha)
                        painter.setPen(QPen(color, 1))
                        painter.drawLine(int(node['x']), int(node['y']), 
                                       int(other['x']), int(other['y']))
        
        # Draw nodes
        for node in self.neural_nodes:
            size = node['size'] + int(3 * node['energy'])
            pulse_alpha = int(100 * (math.sin(node['pulse']) + 1) * 0.5)
            
            # Node glow
            glow_color = QColor(0, 255, 255, pulse_alpha)
            painter.setBrush(QBrush(glow_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(node['x'] - size - 2), int(node['y'] - size - 2), 
                              size * 2 + 4, size * 2 + 4)
            
            # Node core
            core_color = QColor(0, 255, 255, 200)
            painter.setBrush(QBrush(core_color))
            painter.drawEllipse(int(node['x'] - size), int(node['y'] - size), 
                              size * 2, size * 2)
        
        # Draw synaptic firings
        for firing in self.synaptic_firings[:]:
            alpha = int(255 * firing['life'] / firing['max_life'])
            color = firing['color']
            color.setAlpha(alpha)
            painter.setPen(QPen(color, 2))
            painter.setBrush(QBrush(color))
            
            node = firing['node']
            size = node['size'] + 5
            painter.drawEllipse(int(node['x'] - size), int(node['y'] - size), 
                              size * 2, size * 2)
            
            firing['life'] -= 1
            if firing['life'] <= 0:
                self.synaptic_firings.remove(firing)

    def paint_data_streams(self, painter):
        """Paint flowing data streams"""
        for stream in self.data_streams:
            # Calculate current position
            x = stream['start_x'] + (stream['end_x'] - stream['start_x']) * stream['progress']
            y = stream['start_y'] + (stream['end_y'] - stream['start_y']) * stream['progress']
            
            # Draw data stream line
            color = stream['color']
            color.setAlpha(int(100 * stream['glow']))
            painter.setPen(QPen(color, stream['width']))
            painter.drawLine(int(stream['start_x']), int(stream['start_y']), 
                           int(x), int(y))
            
            # Draw data bits
            for i, bit in enumerate(stream['data']):
                if i < 20:  # Only show first 20 bits
                    bit_x = x - i * 8
                    bit_y = y
                    if 0 <= bit_x <= self.width():
                        bit_color = QColor(255, 255, 255, 150)
                        painter.setPen(QPen(bit_color, 1))
                        painter.drawText(int(bit_x), int(bit_y), bit)

    def paint_glitch_effects(self, painter):
        """Paint glitch and corruption effects"""
        # Draw glitch lines
        for line in self.glitch_lines:
            alpha = int(255 * line['life'] / line['max_life'])
            color = line['color']
            color.setAlpha(alpha)
            painter.fillRect(int(line['x']), int(line['y']), 
                           line['width'], line['height'], color)
        
        # Draw glitch blocks
        for block in self.glitch_blocks:
            alpha = int(255 * block['life'] / block['max_life'])
            color = block['color']
            color.setAlpha(alpha)
            painter.fillRect(int(block['x']), int(block['y']), 
                           block['size'], block['size'], color)

    def paint_holographic_elements(self, painter):
        """Paint holographic UI elements"""
        # Draw holographic rings
        for ring in self.hologram_rings:
            alpha = int(ring['alpha'] * (math.sin(ring['pulse']) + 1) * 0.5)
            color = ring['color']
            color.setAlpha(alpha)
            painter.setPen(QPen(color, ring['thickness']))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            
            painter.save()
            painter.translate(ring['center_x'], ring['center_y'])
            painter.rotate(ring['rotation'] * 180 / math.pi)
            painter.drawEllipse(-ring['radius'], -ring['radius'], 
                              ring['radius'] * 2, ring['radius'] * 2)
            painter.restore()
            
        # Draw holographic texts
        font = QFont("Arial", 10)
        painter.setFont(font)
        
        for text in self.hologram_texts:
            if text['glitch'] > 0.8:
                # Apply glitch effect
                offset = random.randint(-2, 2)
                text['x'] += offset
            
            color = text['color']
            color.setAlpha(text['alpha'])
            painter.setPen(QPen(color, 1))
            
            painter.save()
            painter.translate(text['x'], text['y'])
            painter.scale(text['scale'], text['scale'])
            painter.rotate(text['rotation'] * 180 / math.pi)
            painter.drawText(0, 0, text['text'])
            painter.restore()

    def paint_scanning_effects(self, painter):
        """Paint scanning and security effects"""
        # Draw scan lines
        for scan in self.scan_lines:
            alpha = int(120 * scan['glow'])
            color = scan['color']
            color.setAlpha(alpha)
            painter.fillRect(0, int(scan['y']), scan['width'], scan['height'], color)
            
        # Draw radar sweeps
        for radar in self.radar_sweeps:
            painter.save()
            painter.translate(radar['center_x'], radar['center_y'])
            painter.rotate(radar['angle'] * 180 / math.pi)
        
            # Create radar sweep path
            path = QPainterPath()
            path.moveTo(0, 0)
            path.arcTo(-radar['radius'], -radar['radius'], 
                      radar['radius'] * 2, radar['radius'] * 2, 0, 45)
            path.lineTo(0, 0)
            
            color = radar['color']
            painter.setPen(QPen(color, radar['thickness']))
            painter.setBrush(QBrush(color))
            painter.drawPath(path)
            painter.restore()

    def paint_particle_systems(self, painter):
        """Paint particle effects"""
        # Draw energy particles
        for particle in self.energy_particles:
            alpha = int(particle['alpha'] * particle['life'] / particle['max_life'])
            color = particle['color']
            color.setAlpha(alpha)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(particle['x'] - particle['size']), 
                              int(particle['y'] - particle['size']), 
                              particle['size'] * 2, particle['size'] * 2)
        
        # Draw digital dust
        for dust in self.digital_dust:
            alpha = int(dust['color'].alpha() * dust['life'] / dust['max_life'])
            color = dust['color']
            color.setAlpha(alpha)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(dust['x'] - dust['size']), 
                              int(dust['y'] - dust['size']), 
                              dust['size'] * 2, dust['size'] * 2)

    def paint_audio_visualization(self, painter):
        """Paint simulated audio visualization"""
        # Draw audio spectrum bars
        bar_width = self.width() / len(self.audio_spectrum)
        for i, height in enumerate(self.audio_spectrum):
            bar_height = height * 100
            x = i * bar_width
            y = self.height() - bar_height
            
            color = QColor(0, 255, 255, int(200 * height))
            painter.fillRect(int(x), int(y), int(bar_width - 1), int(bar_height), color)
        
        # Draw bass drops
        for drop in self.bass_drops:
            alpha = int(drop['color'].alpha() * drop['life'] / 60)
            color = drop['color']
            color.setAlpha(alpha)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(drop['x'] - drop['size']), 
                              int(drop['y'] - drop['size']), 
                              drop['size'] * 2, drop['size'] * 2)

    def resizeEvent(self, event):
        """Handle widget resize"""
        super().resizeEvent(event)
        # Reinitialize systems with new dimensions
        self.init_matrix_rain()
        self.init_neural_network()
        self.init_data_streams()
        self.init_glitch_effects()
        self.init_holographic_elements()
        self.init_scanning_effects()
        self.init_particle_systems()
        self.init_audio_visualization()

# Alias for backward compatibility
AnimatedBackgroundWidget = CyberpunkHackerBackground 
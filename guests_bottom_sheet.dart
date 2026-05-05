import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

/// Upper limits for guest counts (hotel search): min 1 adult, max [kHotelGuestMaxAdults]
/// adults / [kHotelGuestMaxChildren] children. With 3 adults, children must be 0.
const int kHotelGuestMaxAdults = 3;
const int kHotelGuestMaxChildren = 2;

/// Returns `null` if valid; otherwise a message for SnackBars / inline errors.
String? hotelGuestCombinationError(int adults, int children) {
  if (adults < 1) {
    return 'At least 1 adult is required.';
  }
  if (adults > kHotelGuestMaxAdults) {
    return 'You can select at most $kHotelGuestMaxAdults adults.';
  }
  if (children < 0) {
    return 'Invalid number of children.';
  }
  if (children > kHotelGuestMaxChildren) {
    return 'You can select at most $kHotelGuestMaxChildren children.';
  }
  if (adults == kHotelGuestMaxAdults && children > 0) {
    return 'When 3 adults are selected, you cannot add children.';
  }
  return null;
}

class GuestsBottomSheet extends StatefulWidget {
  final int rooms;
  final int adults;
  final int children;

  const GuestsBottomSheet({
    super.key,
    required this.rooms,
    required this.adults,
    required this.children,
  });

  @override
  State<GuestsBottomSheet> createState() => _GuestsBottomSheetState();
}

class _GuestsBottomSheetState extends State<GuestsBottomSheet> {
  late int _rooms;
  late int _adults;
  late int _children;
  String? _applyError;

  @override
  void initState() {
    super.initState();
    _rooms = widget.rooms;
    _adults = widget.adults.clamp(1, kHotelGuestMaxAdults);
    _children = widget.children.clamp(0, kHotelGuestMaxChildren);
  }

  void _onCountersChanged(VoidCallback fn) {
    setState(() {
      _applyError = null;
      fn();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: AppTheme.backgroundBlack,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
        border: Border.all(color: AppTheme.primaryGold.withOpacity(0.2), width: 0.5),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Drag handle
          Center(
            child: Container(
              margin: const EdgeInsets.only(top: 12),
              width: 40, height: 4,
              decoration: BoxDecoration(
                color: AppTheme.textDim,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),

          // Cancel button
          Align(
            alignment: Alignment.centerLeft,
            child: TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text(
                'Cancel',
                style: TextStyle(
                  color: AppTheme.primaryGold,
                  fontSize: 16,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ),
          ),

          // Title
          const Padding(
            padding: EdgeInsets.fromLTRB(24, 8, 24, 32),
            child: Text(
              'Select rooms\nand guests',
              style: TextStyle(
                color: AppTheme.textWhite,
                fontSize: 30,
                fontWeight: FontWeight.w800,
                height: 1.2,
              ),
            ),
          ),

          // Rooms row
          _CounterRow(
            label: 'Rooms',
            isBold: true,
            value: _rooms,
            min: 1,
            max: 10,
            onDecrement: () => _onCountersChanged(() => _rooms--),
            onIncrement: () => _onCountersChanged(() => _rooms++),
          ),

          Divider(color: AppTheme.primaryGold.withOpacity(0.12),
              indent: 24, endIndent: 24, height: 1),

          // Adults row
          _CounterRow(
            label: 'Adults',
            isBold: false,
            value: _adults,
            min: 1,
            max: kHotelGuestMaxAdults,
            onDecrement: () => _onCountersChanged(() => _adults--),
            onIncrement: () => _onCountersChanged(() => _adults++),
          ),

          // Children row
          _CounterRow(
            label: 'Children (0–17)',
            isBold: false,
            value: _children,
            min: 0,
            max: kHotelGuestMaxChildren,
            onDecrement: () => _onCountersChanged(() => _children--),
            onIncrement: () => _onCountersChanged(() => _children++),
          ),

          if (_applyError != null)
            Padding(
              padding: const EdgeInsets.fromLTRB(24, 16, 24, 0),
              child: Text(
                _applyError!,
                style: const TextStyle(
                  color: Color(0xFFE57373),
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                  height: 1.35,
                ),
              ),
            ),

          Divider(color: AppTheme.primaryGold.withOpacity(0.12),
              indent: 24, endIndent: 24, height: 1),

          const SizedBox(height: 32),

          // Apply button
          Padding(
            padding: const EdgeInsets.fromLTRB(24, 0, 24, 40),
            child: SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton(
                onPressed: () {
                  final err =
                      hotelGuestCombinationError(_adults, _children);
                  if (err != null) {
                    setState(() => _applyError = err);
                    return;
                  }
                  Navigator.pop(context, {
                    'rooms': _rooms,
                    'adults': _adults,
                    'children': _children,
                  });
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryGold,
                  foregroundColor: AppTheme.backgroundBlack,
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text(
                  'Apply',
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ─── Counter row widget ───────────────────────────────────────────────────────
class _CounterRow extends StatelessWidget {
  final String label;
  final bool isBold;
  final int value;
  final int min;
  final int max;
  final VoidCallback onDecrement;
  final VoidCallback onIncrement;

  const _CounterRow({
    required this.label,
    required this.isBold,
    required this.value,
    required this.min,
    required this.max,
    required this.onDecrement,
    required this.onIncrement,
  });

  @override
  Widget build(BuildContext context) {
    final canDecrement = value > min;
    final canIncrement = value < max;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 18),
      child: Row(
        children: [
          Expanded(
            child: Text(
              label,
              style: TextStyle(
                color: isBold ? AppTheme.textWhite : AppTheme.textMuted,
                fontSize: 17,
                fontWeight: isBold ? FontWeight.w700 : FontWeight.w500,
              ),
            ),
          ),
          // Decrement button
          _CircleButton(
            icon: Icons.remove,
            enabled: canDecrement,
            onTap: canDecrement ? onDecrement : null,
          ),
          // Value
          SizedBox(
            width: 40,
            child: Center(
              child: Text(
                '$value',
                style: const TextStyle(
                  color: AppTheme.primaryGold,
                  fontSize: 20,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ),
          ),
          // Increment button
          _CircleButton(
            icon: Icons.add,
            enabled: canIncrement,
            onTap: canIncrement ? onIncrement : null,
          ),
        ],
      ),
    );
  }
}

class _CircleButton extends StatelessWidget {
  final IconData icon;
  final bool enabled;
  final VoidCallback? onTap;

  const _CircleButton({
    required this.icon,
    required this.enabled,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 36, height: 36,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          border: Border.all(
            color: enabled
                ? AppTheme.primaryGold.withOpacity(0.6)
                : AppTheme.textDim.withOpacity(0.3),
            width: 1.5,
          ),
          color: Colors.transparent,
        ),
        child: Icon(
          icon,
          size: 18,
          color: enabled ? AppTheme.primaryGold : AppTheme.textDim,
        ),
      ),
    );
  }
}